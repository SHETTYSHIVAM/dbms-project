import React from "react";
import { FaTimes } from "react-icons/fa";
import { NavLink } from "react-router-dom";
function SideBar({sidebarOpen, toggleSidebar}) {
    const sidebarItems = [
      {path: '/dashboard', label: 'Dashboard',},
      {path: '/my-listings', label: 'My Listings'},
      {path: '/books-requested', label: 'Books Requested'},
      {path: '/settings', label: 'Settings'},
      {path: '/help', label: 'Help'},
    ]
  return (
    <div
      className={`absolute z-50 top-0 left-0 w-64 bg-white dark:bg-zinc-700 dark:text-gray-100 shadow-lg h-screen m-0 transform ${
        sidebarOpen ? "translate-x-0" : "-translate-x-full"
      } transition-transform duration-300`}
    >
      <div className="p-4">
        <FaTimes
          size={24}
          onClick={toggleSidebar}
          className="cursor-pointer absolute top-4 right-4"
        />
        <nav className="flex flex-col mt-12 gap-6">
          {sidebarItems.map(({ path, label }) => (
            <NavLink
              key={path}
              to={path}
              className="text-lg"
              onClick={() => setSidebarOpen(false)} // Close sidebar on click
            >
              <p>{label}</p>

            </NavLink>
          ))}
        </nav>
      </div>
    </div>
  );
}

export default SideBar;
