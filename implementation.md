#### **Configurações**
Adicione ao seu `IServiceCollection` via `services.ConfigureMetrics()` no `Startup` da aplicação ou `Program`. 

```csharp
services.ConfigureMetrics();
```

#### **Implementação**
Adicione ao seu `IApplicationBuilder` via `app.UseMetrics()` no `Startup` da aplicação ou `Program`. 

```csharp
app.UseMetrics();
```

Sua aplicação irá expor um endpoint `/metrics`.

#### Definindo o nome da métrica

Para definir o nome da métrica, siga a convenção definida na [documentação do prometheus](https://prometheus.io/docs/practices/naming/#metric-names).

