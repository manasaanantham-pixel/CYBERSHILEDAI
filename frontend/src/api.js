
const API_URL = "http://127.0.0.1:8000";

export { API_URL };




export async function apiFetch(
  endpoint,
  options = {}
) {

  const token = localStorage.getItem(
    "access_token"
  );



  const headers = {
    ...(options.headers || {})
  };



  if (token) {

    headers.Authorization =
      `Bearer ${token}`;

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

    throw new Error(
      "Unable to connect to CyberShield AI backend. Make sure FastAPI is running."
    );

  }


  

  const text =
    await response.text();

  let data = {};

  if (text) {

    try {

      data = JSON.parse(text);

    } catch {

      throw new Error(
        "Backend returned invalid JSON."
      );

    }

  }


  

  if (response.status === 401) {

    localStorage.removeItem(
      "access_token"
    );

    localStorage.removeItem(
      "user"
    );

    throw new Error(
      data.detail ||
      "Your session expired. Please login again."
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