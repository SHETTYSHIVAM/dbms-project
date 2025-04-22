import React, { useEffect, useState } from "react";
import { useAuth } from "../../context/AuthContext";
import axiosInstance from "../../../axios";
import moment from "moment";

const ThemeToggle = () => {
  const [isDark, setIsDark] = useState(() => {
    return localStorage.getItem("theme") === "dark";
  });

  useEffect(() => {
    const root = window.document.documentElement;
    if (isDark) {
      root.classList.add("dark");
      localStorage.setItem("theme", "dark");
    } else {
      root.classList.remove("dark");
      localStorage.setItem("theme", "light");
    }
  }, [isDark]);

  return (
    <button
      onClick={() => setIsDark(!isDark)}
      className="ml-auto mb-4 px-4 py-2 text-sm rounded bg-gray-200 dark:bg-gray-700 dark:text-white shadow hover:bg-gray-300 dark:hover:bg-gray-600 transition"
    >
      {isDark ? "☀ Light Mode" : "🌙 Dark Mode"}
    </button>
  );
};

const Profile = () => {
  const [profileData, setProfileData] = useState(null);
  const { handleLogout } = useAuth();

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        const response = await axiosInstance.get("/auth/user");
        if (response.status === 200) {
          setProfileData(response.data);
        } else {
          console.error("Failed to fetch profile data:", response.statusText);
        }
      } catch (error) {
        console.error("Error fetching profile data:", error);
      }
    };
    fetchUserData();
  }, []);

  const {
    user,
    borrowed_books = [],
    fines = [],
    reservations = [],
  } = profileData || {};

  return (
    <div className="min-h-screen bg-gray-100 dark:bg-gray-950 p-6">
      <div className="max-w-7xl mx-auto">
        <ThemeToggle />
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {/* Left: User Info */}
          <div className="bg-white dark:bg-zinc-800 text-gray-900 dark:text-gray-100 p-6 rounded-lg shadow-md md:col-span-1">
            <div className="text-center">
              <div className="w-32 h-32 mx-auto rounded-full bg-orange-400 mb-4 flex items-center justify-center text-4xl font-bold text-white">
                {user?.name?.charAt(0).toUpperCase() || "U"}
              </div>
              <div className="space-y-3">
                <div className="flex justify-between border-b border-gray-300 dark:border-gray-600 pb-2">
                  <span className="text-gray-500">Name:</span>
                  <span className="font-semibold">{user?.name}</span>
                </div>
                <div className="flex justify-between border-b border-gray-300 dark:border-gray-600 pb-2">
                  <span className="text-gray-500">Email:</span>
                  <span className="font-semibold">{user?.email}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-500">User Type:</span>
                  <span className="font-semibold capitalize">
                    {user?.user_type}
                  </span>
                </div>
              </div>
              <button
                onClick={handleLogout}
                className="mt-6 bg-red-500 hover:bg-red-600 text-white w-full py-2 rounded transition"
              >
                Logout
              </button>
            </div>
          </div>

          {/* Right: Transactions */}
          <div className="bg-white dark:bg-zinc-800 text-gray-900 dark:text-gray-100 p-6 rounded-lg shadow-md md:col-span-2 space-y-8">
            {/* Borrowed Books */}
            <section>
              <h3 className="text-xl font-semibold mb-4 border-b border-gray-300 dark:border-gray-600 pb-2">
                📚 Borrowed Books
              </h3>
              {borrowed_books.length === 0 ? (
                <p className="text-gray-500">No books borrowed currently.</p>
              ) : (
                <div className="space-y-4">
                  {borrowed_books.map((book) => (
                    <div
                      key={book.id}
                      className="p-4 border rounded-md bg-gray-50 dark:bg-gray-700 border-gray-300 dark:border-gray-600"
                    >
                      <p>
                        <strong>Copy ID:</strong> {book.copy_id}
                      </p>
                      <p>
                        <strong>Issue Date:</strong>{" "}
                        {moment(book.issue_date).format("MMM DD, YYYY")}
                      </p>
                      <p>
                        <strong>Due Date:</strong>{" "}
                        {moment(book.due_date).format("MMM DD, YYYY")}
                      </p>
                      <p>
                        <strong>Returned:</strong>{" "}
                        {book.is_returned ? "Yes" : "No"}
                      </p>
                      <p>
                        <strong>Fine:</strong> ₹{book.fine.toFixed(2)}
                      </p>
                    </div>
                  ))}
                </div>
              )}
            </section>

            {/* Fines */}
            <section>
              <h3 className="text-xl font-semibold mb-4 border-b border-gray-300 dark:border-gray-600 pb-2">
                💸 Fines
              </h3>
              {fines.length === 0 ? (
                <p className="text-gray-500">No pending fines.</p>
              ) : (
                <ul className="list-disc list-inside">
                  {fines.map((fine, idx) => (
                    <li key={idx}>
                      {fine.description} — ₹{fine.amount}
                    </li>
                  ))}
                </ul>
              )}
            </section>

            {/* Reservations */}
            <section>
              <h3 className="text-xl font-semibold mb-4 border-b border-gray-300 dark:border-gray-600 pb-2">
                📌 Reservations
              </h3>
              {reservations.length === 0 ? (
                <p className="text-gray-500">No current reservations.</p>
              ) : (
                <ul className="list-disc list-inside">
                  {reservations.map((res, idx) => (
                    <li key={idx}>
                      {res.book_name || "Reserved Book"} — Reserved on{" "}
                      {moment(res.date_reserved).format("MMM DD, YYYY")}
                    </li>
                  ))}
                </ul>
              )}
            </section>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Profile;
