import React, { useEffect, useState } from "react";
import { FaRightToBracket } from "react-icons/fa6";
import BookCard from "./BookCard";
import axiosInstance from "../../../axios";

const categories = [
  { name: "B.TECH", count: 2500, icon: "👤" },
  { name: "BSC", count: 1400, icon: "📘" },
  { name: "GENERALS", count: 2500, icon: "📗" },
  { name: "MSC", count: 2500, icon: "📙" },
  { name: "NOVELS", count: 2500, icon: "📘" },
];

export default function BookLibrary() {
  const [books, setBooks] = useState([]);

  useEffect(() => {
    const fetchBooks = async () => {
      try {
        const response = await axiosInstance.get("books/");
        const data = response.data;
        if (response.status !== 200) {
          console.error("Failed to fetch books:", response.statusText);
          return;
        }
        setBooks(data);
      } catch (error) {
        console.error("Error fetching books:", error);
      }
    };

    fetchBooks();
  }, []);

  return (
    <div className="p-6 md:px-12 bg-neutral-950 min-h-screen text-white space-y-12">
      {/* Header and Categories */}
      <div className="flex flex-wrap gap-4 items-center">
        {categories.map((cat, idx) => (
          <button
            key={idx}
            className={`rounded-2xl px-5 py-3 flex items-center gap-2 transition-all duration-200 shadow-sm border text-sm font-medium 
              ${
                idx === 0
                  ? "bg-yellow-200 text-yellow-900 border-yellow-300"
                  : "bg-zinc-800 hover:bg-zinc-700 border-zinc-600 text-white"
              }`}
          >
            <span className="text-base font-semibold">{cat.icon}</span>
            <span>{cat.name}</span>
            <span className="text-sm text-zinc-400">{cat.count} books</span>
          </button>
        ))}
        <button className="ml-auto bg-orange-500 hover:bg-orange-600 text-white px-4 py-2 rounded-xl text-sm font-semibold flex items-center gap-2 transition-all">
          <FaRightToBracket />
          Manage Books
        </button>
      </div>

      {/* Book Grid */}
      {books.length > 0 ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-8">
          {books.map((book) => (
            <BookCard key={book.id} book={book} />
          ))}
        </div>
      ) : (
        <div className="flex items-center justify-center h-64 text-gray-400 italic">
          No books available.
        </div>
      )}
    </div>
  );
}
