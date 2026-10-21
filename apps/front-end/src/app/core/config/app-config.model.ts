export interface AppConfig {

    apiUrl: string;
    authUrl: string;

    production: boolean;

    appName: string;
    version: string;

    features: {
        enableDebugTools: boolean;
        enableExperimentalFeatures: boolean;
    }
}
