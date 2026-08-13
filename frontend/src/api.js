const API_URL = "https://cybershiledai-gg60.onrender.com";

export { API_URL };

export async function apiFetch(endpoint, options = {}) {
    const token = localStorage.getItem("access_token");

    const headers = {
        ...(options.headers || {})
    };

    if (token) {
        headers.Authorization = `Bearer ${token}`;
    }

    let response;

    try {
        response = await fetch(
            `${API_URL}${endpoint}`,
            {
                ...options,
                headers
            }
        );
    } catch (error) {
        console.error(
            "CyberShield AI connection error:",
            error
        );

        throw new Error(
            "Unable to connect to CyberShield AI backend."
        );
    }

    const text = await response.text();

    let data = {};

    if (text) {
        try {
            data = JSON.parse(text);
        } catch (error) {
            console.error(
                "Invalid JSON from backend:",
                text
            );

            throw new Error(
                "Backend returned invalid JSON."
            );
        }
    }

    if (response.status === 401) {
        localStorage.removeItem("access_token");
        localStorage.removeItem("user");

        throw new Error(
            data.detail ||
            "Invalid email or password."
        );
    }

    if (!response.ok) {
        throw new Error(
            data.detail ||
            `Request failed with status ${response.status}.`
        );
    }

    return data;
}
