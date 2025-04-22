 import React from "react";
    import { IoMdDownload, IoMdSearch, IoMdArrowDropdown } from "react-icons/io";
    import { BooksTable } from "./BooksTable";

    function ManageBooks() {
    return (
        <div className="mt-8 p-8 space-y-6 bg-gray-200 dark:bg-gray-900">
        <div className="flex justify-between p-2 my-4">
            <h1 className="text-2xl font-semibold dark:text-gray-50 text-gray-500">
            Manage Books
            </h1>
            <button className="flex bg-orange-400 px-4 py-2 rounded-lg items-center gap-2 font-bold text-white">
            Download <IoMdDownload />
            </button>
        </div>
        <div className="bg-gray-50 rounded-lg dark:bg-zinc-700 text-gray-700 p-4 dark:text-gray-50">
            <div className="flex w-full flex-wrap items-center justify-between px-4">
            <h2 className="text-xl text-gray-700 font-semibold dark:text-gray-50">
                Book Listing
            </h2>
            <h3 className="text-md text-gray-400 dark:text-gray-200">
                2300 Total
            </h3>
            <div className="flex items-center bg-gray-200 shadow-sm dark:bg-zinc-600 text-gray-500 dark:text-gray-200 rounded-sm px-4 w-full max-w-md">
                <IoMdSearch size={20} className="mr-3" />
                <input
                type="text"
                placeholder="Search anything..."
                className="bg-gray-200 dark:bg-zinc-600 text-gray-700 dark:text-gray-200 rounded-sm px-4 py-2 w-full max-w-md"
                />
            </div>
            <div className="flex active:scale-95 items-center dark:bg-zinc-600 dark:hover:bg-zinc-500 transition-colors hover:bg-gray-100 py-2 px-4 rounded-lg">
                <p>Sort By</p>
                <IoMdArrowDropdown/>
            </div>
            <button className="px-4 py-2 border-2 border-gray-500 hover:bg-gray-200 dark:hover:bg-zinc-500 active:scale-95 font-semibold transition-colors">
                Add New Book
            </button>
            </div>
            <BooksTable/>
        </div>
        </div>
    );
    }

    export default ManageBooks;