import axios from "axios";

const API_URL = "http://127.0.0.1:8000/api";

const api = axios.create({
  baseURL: API_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("access_token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const authAPI = {
  login: async (username: string, password: string) => {
    const response = await axios.post(`${API_URL}/login/`, {
      username,
      password,
    });

    localStorage.setItem("access_token", response.data.access);
    localStorage.setItem("refresh_token", response.data.refresh);
    return response.data;
  },

  register: (userData: any) => axios.post(`${API_URL}/register/`, userData),

  logout: () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
  },
};

export const quizAPI = {
  getConceptMap: () => api.get("/concept-map/"),
  getMistakeLinks: () => api.get("/mistakes/links/"),
  resetGlobalProgress: () => api.post("/reset/global/", {}),

  getNextQuestion: (conceptId?: number | null) => {
    if (conceptId) {
      return api.get(`/question/next/?concept_id=${conceptId}`);
    }
    return api.get("/question/next/");
  },

  submitAnswer: (questionId: number, selectedOption: string) =>
    api.post("/submit/", {
      question_id: questionId,
      selected_option: selectedOption,
    }),

  restartConcept: (conceptId: number) =>
    api.post("/concept/restart/", { concept_id: conceptId }),

  getHistory: (conceptId: number) => api.get(`/concept/${conceptId}/history/`),
};

export default api;
