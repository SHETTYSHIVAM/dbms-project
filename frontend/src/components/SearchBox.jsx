import React from "react";
import {IoSearch} from "react-icons/io5";

function SearchBox({value, setValue}) {
    return (
        <div
            className="hidden lg:flex items-center bg-gray-200 dark:bg-zinc-800 text-gray-500 dark:text-gray-200 rounded-lg p-2 w-full max-w-md">
            <IoSearch size={20} className="mr-3"/>
            <input
                className="text-sm px-4"
                value={value}
                onChange={(e) => setValue(e.target.value)}
                placeholder="Search anything..."
            ></input>
        </div>
    );
}

export default SearchBox;
