import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { AppConfig } from './app-config.model';
import { firstValueFrom } from 'rxjs';

/**
 * Service to load and provide application configuration settings.
 * @usage
 * In Angular main.ts, add the following to the providers settings:
 *
 * ```Angular
 * private readonly appConfigService = inject(AppConfigService);
 * console.log('AppConfigService settings:', appConfigService.settings);
 * ```
 * @returns {AppConfigService} An instance of the AppConfigService.
 */
@Injectable({
    providedIn: 'root',
})
export class AppConfigService {

    private readonly http = inject(HttpClient);

    private config!: AppConfig;

    async load(): Promise<void> {
        this.config = await firstValueFrom(
            this.http.get<AppConfig>('config/config.json')
        )
    };

    get settings(): AppConfig {
        if (!this.config) {
            throw new Error('AppConfigService not initialized.');
        }
        return this.config;
    }

    get apiUrl(): string {
        return this.settings.apiUrl;
    }

    get authUrl(): string {
        return this.settings.authUrl;
    }

    get production(): boolean {
        return this.settings.production;
    }

    get appName(): string {
        return this.settings.appName;
    }

    get version(): string {
        return this.settings.version;
    }

    get features(): { enableDebugTools: boolean; enableExperimentalFeatures: boolean } {
        return this.settings.features;
    }
}
