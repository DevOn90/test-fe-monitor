import { BaseInstrumentation } from '@grafana/faro-core';

export class LongTaskInstrumentation extends BaseInstrumentation {
  readonly name = 'long-task-instrumentation';
  readonly version = '1.0.0';

  private observer?: PerformanceObserver;

  initialize(): void {
    // Check whether the browser supports Long Task observation.
    if (
      typeof PerformanceObserver === 'undefined' ||
      !PerformanceObserver.supportedEntryTypes?.includes('longtask')
    ) {
      return;
    }

    this.observer = new PerformanceObserver((list) => {
      for (const entry of list.getEntries()) {
        this.api.pushEvent(
          'faro.performance.longtask',
          {
            duration_ms: entry.duration.toFixed(2),
            start_time_ms: entry.startTime.toFixed(2),
            entry_name: entry.name,
            entry_type: entry.entryType,
          },
          'browser'
        );
      }
    });

    this.observer.observe({
      type: 'longtask',
      buffered: true,
    });
  }

  destroy(): void {
    this.observer?.disconnect();
    this.observer = undefined;
  }
}