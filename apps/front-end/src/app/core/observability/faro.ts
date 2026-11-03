import { initializeFaro, getWebInstrumentations } from '@grafana/faro-web-sdk';
import { TracingInstrumentation } from '@grafana/faro-web-tracing'
import { ResourceErrorsInstrumentation } from './instrumentations/resource-errors.instrumentation';

export function initializeFrontendMonitoring(): void {
  initializeFaro({
    url: 'http://localhost:12345/collect',
    app: {
      name: 'front-end',
      version: '1.0.0',
    },
    instrumentations: [
      ...getWebInstrumentations(),
      new TracingInstrumentation(),
      new ResourceErrorsInstrumentation(),
    ],
  });
}