import React, { useEffect, useState } from "react";
import { FaRightToBracket } from "react-icons/fa6";
import BookCard from "./BookCard";
import axiosInstance from "../../../axios";
import SearchBox from "../SearchBox";
export default function BookLibrary() {
  const [books, setBooks] = useState([]);
  const [filters, setFilters] = useState({
    author: "",
    subject: "",
    language: "",
    published_year: "",
    publisher: "",
    title: "",
  });

  const [searchText, setSearchText] = useState("");

  const fetchBooks = async () => {
    try {
      const params = new URLSearchParams();

      Object.entries(filters).forEach(([key, value]) => {
        if (value) params.append(key, value);
      });
      const response = await axiosInstance.get(`books/?${params.toString()}`);
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

  useEffect(() => {
    fetchBooks();
  }, []);

  return (
    <div className="p-6 md:px-12 bg-neutral-950 min-h-screen text-white space-y-12">
      {/* Header and Categories */}
      <div className="flex flex-wrap gap-4 items-center">
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4 w-full">
          {Object.entries(filters).map(([key, value]) => (
            <input
              key={key}
              type="text"
              className="bg-zinc-800 text-white border border-zinc-600 rounded-xl px-3 py-2 text-sm placeholder-zinc-400"
              placeholder={key
                .replace("_", " ")
                .replace(/\b\w/g, (l) => l.toUpperCase())}
              value={value}
              onChange={(e) =>
                setFilters((prev) => ({ ...prev, [key]: e.target.value }))
              }
            />
          ))}
        </div>
        <div className="flex items-center justify-between p-4 gap-4">
          <SearchBox value={searchText} setValue={setSearchText} />
          <button
            onClick={fetchBooks}
            className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-xl text-sm font-semibold transition-all"
          >
            Search
          </button>
        </div>

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
