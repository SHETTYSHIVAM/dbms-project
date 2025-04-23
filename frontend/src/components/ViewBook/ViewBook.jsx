import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import axiosInstance from "../../../axios";
import { toast } from "react-toastify";

function ViewBook() {
  const { id } = useParams();
  const [book, setBook] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchBook = async () => {
      try {
        const response = await axiosInstance.get(`/books/${id}`);
        setBook(response.data);
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

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-gray-500 dark:text-gray-400 italic">
          Loading...
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
    <div className="flex flex-col lg:flex-row items-center justify-center gap-8 p-8 max-w-5xl mx-auto bg-gray-50 dark:bg-zinc-800 shadow-md">
      <img
        src={book.image_url || "/default-book.png"}
        alt={book.title}
        className="w-72 object-cover rounded-lg shadow-lg"
      />
      <div className="flex flex-col space-y-6 w-full">
        <div className="space-y-4">
          <div className="flex justify-between">
            <h2 className="text-lg font-semibold text-gray-700 dark:text-gray-100">Book Title</h2>
            <p className="text-md text-gray-500 dark:text-gray-300 italic">{book.title}</p>
          </div>
          <div className="flex justify-between">
            <h2 className="text-lg font-semibold text-gray-700 dark:text-gray-100">Author</h2>
            <p className="text-md text-gray-500 dark:text-gray-300 italic">{book.author}</p>
          </div>
          <div className="flex justify-between">
            <h2 className="text-lg font-semibold text-gray-700 dark:text-gray-100">Publisher</h2>
            <p className="text-md text-gray-500 dark:text-gray-300 italic">{book.publisher}</p>
          </div>
          <div className="flex justify-between">
            <h2 className="text-lg font-semibold text-gray-700 dark:text-gray-100">Genre</h2>
            <p className="text-md text-gray-500 dark:text-gray-300 italic">{book.genre}</p>
          </div>
        </div>

        <p className="text-gray-700 dark:text-gray-200 text-justify">{book.description}</p>

        <div className="mt-4 flex flex-wrap items-center gap-3">
          <button className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition">
            Borrow
          </button>
          <button className="px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 transition">
            Reserve
          </button>
          <button className="px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 transition">
            Return
          </button>
        </div>
      </div>
    </div>
  );
}

export default ViewBook;
