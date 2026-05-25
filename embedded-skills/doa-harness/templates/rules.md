# rules/*.md 模板

每条规则文件包含 4 段：规则 + 原因 + 正反例 + 检测方式。
根据探测到的技术栈生成对应规则 + 通用安全规则。

---

## 规则文件结构（标准格式）

```markdown
规则: {rule_name}
原因: {reason}

## 正确 ✅
\`\`\`{language}
{correct_example}
\`\`\`

## 错误 ❌
\`\`\`{language}
{incorrect_example}
\`\`\`

## 检测
{detection_instruction}
```

---

## 通用规则（所有项目都生成）

### rules/no-secrets-in-code.md

```markdown
规则: 禁止在代码中硬编码密钥、token、连接字符串
原因: 防止敏感信息泄露到版本控制系统

## 正确 ✅
\`\`\`
# .NET — 通过配置文件 + 环境变量
var connStr = Configuration.GetConnectionString("Default");

# Node — 通过环境变量
const apiKey = process.env.API_KEY;

# Python — 通过环境变量
api_key = os.environ["API_KEY"]
\`\`\`

## 错误 ❌
\`\`\`
# 任何语言 — 硬编码密钥
const API_KEY = "sk-abc123...";
var connStr = "Server=prod-db;Password=P@ssw0rd";
api_key = "AIzaSyB..."
\`\`\`

## 检测
看到代码中包含疑似密钥的字符串字面量（含 sk-、AIza、password=、connectionstring= 等关键词）
→ 停下改为环境变量或配置文件引用
```

---

## 按技术栈生成的规则

### React / TypeScript

#### rules/react-patterns.md

```markdown
规则: 禁止组件内直接调用 fetch/axios
原因: 绕过统一的请求拦截、错误处理和认证 token 注入

## 正确 ✅
\`\`\`tsx
// 具体实现根据项目探测结果填充
// 如探测到 react-query:
import { useQuery } from '@tanstack/react-query'
import { orderApi } from '@/api'
const { data } = useQuery({ queryKey: ['orders'], queryFn: orderApi.getList })

// 如探测到 umi-request:
import { request } from '@/tools/request'
const data = await request('/api/orders')

// 如探测到 axios 封装:
import { http } from '@/api/http'
const data = await http.get('/orders')
\`\`\`

## 错误 ❌
\`\`\`tsx
useEffect(() => {
  fetch('/api/orders')      // ← 直调，绕过统一请求层
    .then(r => r.json())
    .then(setData)
}, [])
\`\`\`

## 检测
看到 useEffect + fetch/axios 直接调用 → 停下改用项目的请求工具层（{request_layer_path}）
```

#### rules/no-direct-fetch.md

> 如果项目已有 `react-patterns.md` 且内容覆盖了此规则，则跳过不生成。

### Vue / TypeScript

#### rules/vue-patterns.md

```markdown
规则: 禁止 Options API，统一使用 Composition API
原因: 保持代码风格一致，便于逻辑复用

## 正确 ✅
\`\`\`vue
<script setup lang="ts">
import { ref, onMounted } from 'vue'
const count = ref(0)
</script>
\`\`\`

## 错误 ❌
\`\`\`vue
<script>
export default {
  data() { return { count: 0 } },
  methods: { increment() { this.count++ } }
}
</script>
\`\`\`

## 检测
看到 export default { data(), methods } → 停下改为 <script setup>
```

### .NET

#### rules/dotnet-data-access.md

```markdown
规则: Controller 禁止直接注入 DbContext
原因: 绕过业务逻辑层和权限校验

## 正确 ✅
\`\`\`csharp
// 具体实现根据项目架构填充
// 如探测到 MediatR:
public class GetOrdersHandler : IRequestHandler<GetOrdersQuery, List<OrderDto>>
{
    private readonly IOrderRepository _repo;
}

// 如探测到分层架构 (Controller → Service):
public class OrderController : ControllerBase
{
    private readonly IOrderService _service;
    public OrderController(IOrderService service) { _service = service; }
}
\`\`\`

## 错误 ❌
\`\`\`csharp
public class OrderController : ControllerBase
{
    private readonly AppDbContext _db;  // ← Controller 直注 DbContext
    public OrderController(AppDbContext db) { _db = db; }
}
\`\`\`

## 检测
看到 Controller 构造函数注入 DbContext → 停下改用 {service_layer}
```

#### rules/no-lazy-load.md

```markdown
规则: 禁止使用 LazyLoading，必须显式 Include
原因: 避免 N+1 查询导致性能问题

## 正确 ✅
\`\`\`csharp
var orders = await _context.Orders
    .Include(o => o.Items)
    .Include(o => o.Customer)
    .AsSplitQuery()
    .ToListAsync();
\`\`\`

## 错误 ❌
\`\`\`csharp
var orders = await _context.Orders.ToListAsync();
foreach (var order in orders)
{
    var items = order.Items;  // ← N+1 查询
}
\`\`\`

## 检测
看到列表查询没有 Include → 停下添加显式 Include
```

### Python

#### rules/python-imports.md

```markdown
规则: 禁止在路由函数中直接创建数据库 session
原因: 绕过事务管理和连接池

## 正确 ✅
\`\`\`python
@router.get("/users")
async def get_users(service: UserService = Depends(get_user_service)):
    return await service.list_users()
\`\`\`

## 错误 ❌
\`\`\`python
@router.get("/users")
async def get_users():
    session = SessionLocal()  # ← 直接创建 session
    users = session.query(User).all()
    return users
\`\`\`

## 检测
看到路由函数内 SessionLocal() 或 create_engine → 停下改用依赖注入
```

#### rules/no-raw-sql.md

```markdown
规则: 禁止使用 raw SQL，必须通过 ORM
原因: 防止 SQL 注入，保持可移植性

## 正确 ✅
\`\`\`python
users = await session.execute(
    select(User).where(User.age > 18)
)
\`\`\`

## 错误 ❌
\`\`\`python
users = await session.execute(
    text("SELECT * FROM users WHERE age > 18")
)
\`\`\`

## 检测
看到 text("SELECT/INSERT/UPDATE/DELETE") → 停下改用 ORM 查询
```

### Go

#### rules/go-error-handling.md

```markdown
规则: 禁止忽略 error 返回值
原因: Go 的错误处理是显式的，忽略 error 会隐藏问题

## 正确 ✅
\`\`\`go
result, err := doSomething()
if err != nil {
    return fmt.Errorf("doSomething failed: %w", err)
}
\`\`\`

## 错误 ❌
\`\`\`go
result, _ := doSomething()  // ← 忽略 error
\`\`\`

## 检测
看到 `_, _ :=` 或 `_ =` 忽略 error 返回值 → 停下添加错误处理
```

---

## 规则生成决策表

| 技术栈 | 必生成规则 | 可选规则 |
|--------|----------|---------|
| 所有项目 | `no-secrets-in-code.md` | — |
| React/TS | `react-patterns.md` | `no-direct-fetch.md`（与 react-patterns 不重复时） |
| Vue/TS | `vue-patterns.md` | `no-direct-fetch.md` |
| .NET | `dotnet-data-access.md`、`no-lazy-load.md` | — |
| Python | `python-imports.md`、`no-raw-sql.md` | — |
| Go | `go-error-handling.md` | — |

---

## 用户自定义规则

如果用户在交互确认阶段（Step 2）提供了额外编码规约，按以下格式为每条生成独立文件：

1. 文件名：用户提供的规则名转 kebab-case → `rules/{name}.md`
2. 内容：按标准 4 段格式生成，由 AI 根据用户描述补全正反例和检测方式
3. 生成后在 AGENTS.md 的"关键约束"段落中追加引用

---

## 增量更新策略

**更新模式下**（`--update`）：
- 仅生成不存在的规则文件
- 已有规则文件不覆盖（用户可能修改了示例代码以适配项目）
- 如果探测到新的技术栈（如项目新增了 Python 子项目），生成该栈对应的规则
