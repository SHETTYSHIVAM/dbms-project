import React from "react";
import { FaChevronRight } from "react-icons/fa";
import { Link } from "react-router-dom";
const BookCard = ({  book }) => {
  return (
    <Link
      className="relative max-w-md p-4 rounded-2xl shadow-md border border-zinc-300 dark:border-zinc-600 bg-white dark:bg-zinc-800 transition-transform transform hover:-translate-y-1 hover:shadow-xl cursor-pointer"
      to={`/books/${book.isbn}`}
    >
      <div className="overflow-hidden rounded-xl aspect-[3/4] bg-zinc-100 dark:bg-zinc-700">
        <img
        loading="lazy"
          src={book.image_url || "/default-book.png"}
          alt={book.title}
          className="w-full h-full object-cover transition-transform duration-300 hover:scale-105"
        />
      </div>
      <div className="mt-4 text-center space-y-1">
        <h3 className="text-base font-bold text-zinc-800 dark:text-zinc-100 line-clamp-2">{book.title}</h3>
        <p className="text-sm text-zinc-500 dark:text-zinc-400 italic">{book.author}</p>
      </div>
    </Link>
  );
};

export default BookCard;
