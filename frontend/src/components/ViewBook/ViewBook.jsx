import React, {useEffect, useState} from "react";
import {useParams} from "react-router-dom";
import axiosInstance from "../../../axios";
import {toast} from "react-toastify";
import {useAuth} from "../../context/AuthContext";
import Loader from "../Loader";

function ViewBook() {
  const { id } = useParams();
  const [book, setBook] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
    const {user} = useAuth();
    const [buttonDisabled, setButtonDisabled] = useState(false);

  useEffect(() => {
    const fetchBook = async () => {
      try {
        const response = await axiosInstance.get(`/books/${id}`);
        setBook(response.data);
          console.log(response.data);
      } catch (error) {
        console.error("Error fetching book:", error);
        toast.error("Failed to fetch book details.");
        setError(error);
      } finally {
        setLoading(false);
      }
    };
    fetchBook();
  }, [id]);

    const handleReserve = async () => {
        if (!user) {
            toast.error("You need to be logged in to reserve a book.");
            return;
        }

        setButtonDisabled(true); // 🔒 Prevent multiple clicks immediately

        try {
            const response = await axiosInstance.post(`/reservations/`, {
                book_id: id,
            });

            if (response.status !== 201) {
                toast.error("Failed to reserve book. Perhaps it's already reserved.");
                setButtonDisabled(false); // 🔓 Re-enable if failed
                return;
            }

            toast.success("Book reserved successfully!");
        } catch (error) {
            console.error("Error reserving book:", error);
            toast.error("Failed to reserve book.");
            setButtonDisabled(false); // 🔓 Re-enable if error
        }
    };


  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-gray-500 dark:text-gray-400 italic">
            <Loader/>
        </div>
      </div>
    );
  }

  if (error || !book) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-red-500 dark:text-red-400 italic">
          Error loading book details.
        </div>
      </div>
    );
  }

  return (
      <div className="min-h-screen px-4 py-8 bg-gray-50 dark:bg-zinc-800">
          <div
              className="flex flex-col lg:flex-row items-center justify-center gap-8 max-w-5xl mx-auto shadow-md bg-white dark:bg-zinc-900 rounded-lg p-6">
              <img
                  src={book.image_url || "/default-book.png"}
                  alt={book.title}
                  className="w-full max-w-xs object-cover rounded-lg shadow-md"
              />
              <div className="flex flex-col space-y-6 w-full">
                  <div className="space-y-4">
                      <div className="flex justify-between flex-wrap gap-2">
                          <h2 className="text-lg font-semibold text-gray-700 dark:text-gray-100">
                              Book Title
                          </h2>
                          <p className="text-md text-gray-500 dark:text-gray-300 italic">
                              {book.title}
                          </p>
                      </div>
                      <div className="flex justify-between flex-wrap gap-2">
                          <h2 className="text-lg font-semibold text-gray-700 dark:text-gray-100">
                              Author
                          </h2>
                          <p className="text-md text-gray-500 dark:text-gray-300 italic">
                              {book.author}
                          </p>
                      </div>
                      <div className="flex justify-between flex-wrap gap-2">
                          <h2 className="text-lg font-semibold text-gray-700 dark:text-gray-100">
                              Publisher
                          </h2>
                          <p className="text-md text-gray-500 dark:text-gray-300 italic">
                              {book.publisher}
                          </p>
                      </div>
                      <div className="flex justify-between flex-wrap gap-2">
                          <h2 className="text-lg font-semibold text-gray-700 dark:text-gray-100">
                              Genre
                          </h2>
                          <p className="text-md text-gray-500 dark:text-gray-300 italic">
                              {book.genre}
                          </p>
                      </div>
                  </div>

                  <p className="text-gray-700 dark:text-gray-200 text-justify">
                      {book.description}
                  </p>

          <button
              onClick={handleReserve}
              disabled={buttonDisabled}
              className="w-full sm:w-auto px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 transition disabled:opacity-50"
          >
              {buttonDisabled ? "Reserved" : "Reserve"}
          </button>
        </div>
      </div>
    </div>
  );
}

export default ViewBook;
