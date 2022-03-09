#### **Configurações**
Adicione ao seu `IServiceCollection` via `services.ConfigureMetrics()` no `Startup` da aplicação ou `Program`. 

```csharp
services.ConfigureMetrics();
```

Adicione ao seu `IApplicationBuilder` via `app.UseMetrics()` no `Startup` da aplicação ou `Program`. 

- net5.0
```csharp
app.UseMetrics();
```

- net6.0
```csharp
app.UseMetricServer();
app.UseHttpMetrics();
```

Sua aplicação irá expor um endpoint `/metrics`.

#### Definindo o nome da métrica

Para definir o nome da métrica, siga a convenção definida na [documentação do prometheus](https://prometheus.io/docs/practices/naming/#metric-names).