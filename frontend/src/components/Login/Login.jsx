import React, {useState} from "react";
import axiosInstance from "../../../axios";
import {toast} from "react-toastify";
import {useAuth} from "../../context/AuthContext";

const Login = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const { handleLogin } = useAuth();

  const handleSubmit = async () => {
    setLoading(true);

    try {
      console.log("Form submitted with values:", {
        email,
        password,
      });

      const response = await axiosInstance.post("/auth/login", {
        email,
        password,
      });

      if (response.status === 401) {
        toast.error("Invalid credentials. Please try again.");
        return;
      }


      const { access_token, refresh_token, user } = response.data;
      localStorage.setItem("access_token", access_token);
      localStorage.setItem("refresh_token", refresh_token);
      handleLogin({ user, access_token, refresh_token });

      toast.success("🎉 Login successful!");
      // Redirect after login if needed, e.g., navigate('/dashboard');
    } catch (error) {
      console.error("Login failed:", error);
      toast.error("Something went wrong. Please try again later.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="bg-gray-200 dark:bg-gray-900 min-h-screen flex items-center justify-center px-4">
      <div className="w-full max-w-md bg-white dark:bg-zinc-700 text-gray-700 dark:text-gray-100 rounded-lg shadow-md">
        <div className="p-8 space-y-6">
          <h2 className="text-xl font-bold text-center">
            Sign in to your account
          </h2>
          <form
            className="space-y-4"
            onSubmit={(e) => {
              e.preventDefault();
              handleSubmit();
            }}
          >
            <div>
              <label htmlFor="email" className="block mb-2 text-sm font-medium">
                Your email
              </label>
              <input
                type="email"
                id="email"
                className="w-full px-4 py-2 rounded-md border border-gray-300 bg-gray-100 dark:bg-zinc-600 dark:border-gray-600 focus:outline-none focus:ring-2 focus:ring-orange-400"
                placeholder="name@company.com"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </div>

            <div>
              <label
                htmlFor="password"
                className="block mb-2 text-sm font-medium"
              >
                Password
              </label>
              <input
                  type="password"
                id="password"
                placeholder="••••••••"
                className="w-full px-4 py-2 rounded-md border border-gray-300 bg-gray-100 dark:bg-zinc-600 dark:border-gray-600 focus:outline-none focus:ring-2 focus:ring-orange-400"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </div>

            <div className="flex items-center justify-between text-sm">
              
              <a
                href="#"
                className="text-gray-500 hover:underline dark:text-gray-300"
              >
                Forgot password?
              </a>
            </div>

            <button
              type="submit"
              disabled={loading}
              className={`w-full font-semibold py-2 rounded-md transition-colors ${
                loading
                  ? "bg-orange-300 cursor-not-allowed"
                  : "bg-orange-400 hover:bg-orange-500 text-white"
              }`}
            >
              {loading ? "Signing in..." : "Sign in"}
            </button>

            <p className="text-sm text-center text-gray-500 dark:text-gray-300">
              Don’t have an account yet?{" "}
              <a href="#" className="text-orange-500 hover:underline">
                Sign up
              </a>
            </p>
          </form>
        </div>
      </div>
    </section>
  );
};

export default Login;
