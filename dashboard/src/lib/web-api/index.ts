/**
 * Constructs a new URL string for the web API with the given endpoint and optional query params.
 * Assumes queryParams is an object with single or array values.
 */  
export function getQueryURL(endpoint: string, queryParams?: object): string {
    const baseURL = process.env.NEXT_PUBLIC_WEB_API_BASE_URL || "https://localhost/api/v1";

    // Build query string manually so that spaces are properly percent-encoded.
    const queryString = queryParams
        ? Object.entries(queryParams)
            .map(([key, value]) => {
                return Array.isArray(value)
                    ? value.map((subvalue => `${encodeURIComponent(key)}=${encodeURIComponent(subvalue)}`)).join("&")
                    : `${encodeURIComponent(key)}=${encodeURIComponent(value)}`;
            })
            .join("&")
        : "";
    
    return `${baseURL}/${endpoint}?${queryString}`;
}
