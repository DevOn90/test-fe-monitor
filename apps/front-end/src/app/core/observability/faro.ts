import { 
  initializeFaro, 
  getWebInstrumentations,
  WebVitalsInstrumentation,
  UserActionInstrumentation,
} from '@grafana/faro-web-sdk';
import { TracingInstrumentation } from '@grafana/faro-web-tracing'
import { ResourceErrorsInstrumentation } from './instrumentations/resource-errors.instrumentation';
import { LongTaskInstrumentation } from './instrumentations/long-task.instrumentation';

export function initializeFrontendMonitoring(): void {
  initializeFaro({
    url: 'http://localhost:12345/collect',
    app: {
      name: 'front-end',
      version: '1.0.0',
    },
    dedupe: true,
    instrumentations: [
      ...getWebInstrumentations({
        captureConsole: true,
      }),
      new TracingInstrumentation(),
      new ResourceErrorsInstrumentation(),
      new LongTaskInstrumentation(),
      new WebVitalsInstrumentation(),
      new UserActionInstrumentation(),
    ],
  });
}