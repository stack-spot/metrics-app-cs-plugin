## **Visão Geral**

O **metrics-app-cs-plugin** adiciona em uma stack o uso de métricas para aplicações que executam dentro de containers. Gerando métricas, tais como: counter, gauge, histogram e summary.

Para aplicar o plugin execute o comando:
```
$ stk apply plugin skynet-dotnet-stack/metrics-app-cs-plugin
```
#### **Pré-requisitos**
Para utilizar esse plugin é necessário ter uma stack dotnet criada pelo cli do StackSpot que você pode baixar [**aqui**](https://stackspot.com.br/).

Ter instalado:
- .NET 5 ou 6 
- O template base de `rest-app-cs-template` já deverá estar aplicado para você conseguir utilizar este plugin. 

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

#### Criando métricas de negócio para sua aplicação

Agora, basta escolher qual será o tipo da sua métrica. Nossa stack disponibiliza a criação dos seguintes tipos:

- [Counter](#counter)
- [Gauge](#gauge)
- [Summary](#summary)
- [Histogram](#histogram)

#### Counter

***Counter*** é a interface de criação para métricas do tipo "contador". A interface ***Counter*** permite que uma métrica seja incrementada por um valor fixo, que deve ser positivo.
Um contador deve ser utilizado quando você precisa saber o valor absoluto de alguma coisa, como o número de novos clientes inseridos, a quantidade de logins, etc.

Exemplo:

```csharp
    public class CounterExample
    {
        private readonly ICounter _weatherForecastCallsCounter;

        public CounterExample(IMetricsFactory metricsFactory)
        {
            _weatherForecastCallsCounter = metricsFactory.CreateCounterBuilder("api_calls_total")
                .WithTag("uri", "WeatherForecast")
                .WithNamespace("stackspot")
                .WithDescription("Quantidade de chamadas para a API")
                .Build();

            _weatherForecastCallsCounter.Increment();
        }
    }
```

Saída da métrica criada acima no padrão de coleta do Prometheus:

```bash
# HELP stackspot_api_calls_total Quantidade de chamadas para a API
# TYPE stackspot_api_calls_total counter
stackspot_api_calls_total{uri="WeatherForecast"} 1
```

#### Gauge

***Gauge*** é a interface de criação para métricas do tipo medida instantânea. Ela é usada para obter o valor atual de uma definição. Por exemplo, podemos utilizar o ***Gauge*** para mostrar a quantidade de tarefas em execução ou tamanho de uma fila de processos.

Exemplo:

```csharp
    public class GaugeExample
    {
        private readonly Random _rnd = new Random(Environment.TickCount);
        private static readonly string[] Summaries = new[]
        {
            "Freezing", "Bracing", "Chilly", "Cool", "Mild", "Warm", "Balmy", "Hot", "Sweltering", "Scorching"
        };

        private readonly IGauge _lastNumberOfweatherForecastReturned;

        public GaugeExample(IMetricsFactory metricsFactory)
        {
            _lastNumberOfweatherForecastReturned = metricsFactory.CreateGaugeBuilder("last_quantity_returned")
                .WithNamespace("stackspot")
                .Build();

            var weatherForecast = Summaries
                .OrderBy(f => _rnd.NextDouble())
                .Take(_rnd.Next(1, Summaries.Length))
                .ToArray();

            _lastNumberOfweatherForecastReturned.Set(weatherForecast.Length);
        }
    }
```

Saída da métrica criada acima no padrão de coleta do Prometheus:

```bash
# HELP stackspot_last_quantity_returned 
# TYPE stackspot_last_quantity_returned gauge
stackspot_last_quantity_returned 7
```

#### Summary

Uma métrica do tipo **Summary** é utilizada para rastrear eventos distribuídos.
Basicamente, o sumário entrega um contador, a soma dos registros e o valor máximo de um valor registrado.

Como exemplo de uso do **Summary**, há o registro de tamanhos de payloads que são enviados ao servidor. Podemos fazer isso de duas formas:

Exemplo

```csharp
    public class SummaryExample
    {
        private readonly Random _rnd = new Random(Environment.TickCount);
        private static readonly string[] Summaries = new[]
        {
            "Freezing", "Bracing", "Chilly", "Cool", "Mild", "Warm", "Balmy", "Hot", "Sweltering", "Scorching"
        };

        private readonly ISummary _weatherForecastReturnedSummary;

        public SummaryExample(IMetricsFactory metricsFactory)
        {
            _weatherForecastReturnedSummary = metricsFactory.CreateSummaryBuilder("weatherForecast_returned_total")
                .WithQuantiles(0.1, 0.5, 0.98, 0.99)
                .WithNamespace("stackspot")
                .Build();

            var weatherForecast = Summaries
                .OrderBy(f => _rnd.NextDouble())
                .Take(_rnd.Next(1, Summaries.Length))
                .ToArray();

            _weatherForecastReturnedSummary.Observe(weatherForecast.Length);
        }
    }
```

Saída da métrica criada acima no padrão de coleta do Prometheus:

```bash
# HELP stackspot_weatherforecast_returned_total 
# TYPE stackspot_weatherforecast_returned_total summary
stackspot_weatherforecast_returned_total_sum 7
stackspot_weatherforecast_returned_total_count 1
stackspot_weatherforecast_returned_total{quantile="0.1"} 7
stackspot_weatherforecast_returned_total{quantile="0.5"} 7
stackspot_weatherforecast_returned_total{quantile="0.98"} 7
stackspot_weatherforecast_returned_total{quantile="0.99"} 7

```

#### Histogram

O ***Histogram*** é uma interface de criação de sumário. Ele é feito com base em uma determinação e faz uma contagem de registro de acordo com níveis de serviço ("*SLA*") definidos.

Exemplo:

```csharp
    public class HistogramExample
    {
        private readonly Random _rnd = new Random(Environment.TickCount);
        private static readonly string[] Summaries = new[]
        {
            "Freezing", "Bracing", "Chilly", "Cool", "Mild", "Warm", "Balmy", "Hot", "Sweltering", "Scorching"
        };

        private readonly IHistogram _processingTimeHistogram;

        public HistogramExample(IMetricsFactory metricsFactory)
        {
            _processingTimeHistogram = metricsFactory.CreateHistogramBuilder("processing_time_seconds")
                .WithBuckets(0.1, 0.5, 0.7, 0.9, 1)
                .WithNamespace("stackspot")
                .Build();

            var weatherForecast = Summaries
                .OrderBy(f => _rnd.NextDouble())
                .Take(_rnd.Next(1, Summaries.Length))
                .ToArray();

            _processingTimeHistogram.Observe(() =>
            {
                Task.Delay(_rnd.Next(90, 1099)).Wait();
            });
        }
    }
```

Saída da métrica criada acima no padrão de coleta do Prometheus:

```bash
# HELP stackspot_processing_time_seconds 
# TYPE stackspot_processing_time_seconds histogram
stackspot_processing_time_seconds_sum 0.2964567
stackspot_processing_time_seconds_count 1
stackspot_processing_time_seconds_bucket{le="0.1"} 0
stackspot_processing_time_seconds_bucket{le="0.5"} 1
stackspot_processing_time_seconds_bucket{le="0.7"} 1
stackspot_processing_time_seconds_bucket{le="0.9"} 1
stackspot_processing_time_seconds_bucket{le="1"} 1
stackspot_processing_time_seconds_bucket{le="+Inf"} 1
```
