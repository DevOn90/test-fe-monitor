import { BaseInstrumentation } from '@grafana/faro-core';

export class ResourceErrorsInstrumentation extends BaseInstrumentation {
  readonly name = 'resource-errors';
  readonly version = '1.0.0';

  initialize(): void {
    window.addEventListener(
      'error',
      (event: Event) => {
        const target = event.target;

        if (
          target instanceof HTMLImageElement ||
          target instanceof HTMLScriptElement ||
          target instanceof HTMLLinkElement
        ) {
          const resourceUrl =
            target instanceof HTMLImageElement ||
            target instanceof HTMLScriptElement
              ? target.src
              : target.href;

          this.api.pushError(
            new Error(`Resource loading failed: ${resourceUrl}`),
            {
              type: 'ResourceLoadError',
              context: {
                resourceUrl,
                resourceType: target.tagName,
              },
            }
          );
        }
      },
      true
    );
  }
}