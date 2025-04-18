import React, { useEffect, useRef, useState } from "react";
import { Link, NavLink, useLocation } from "react-router-dom";
import { IoMenu, IoSearch } from "react-icons/io5";
import { FaRegUser } from "react-icons/fa";
import { IoIosArrowDown } from "react-icons/io";
import { FaTimes } from "react-icons/fa"; // For closing the sidebar

function Header() {
  const location = useLocation();
  const dropDownRef = useRef(null);

  // 🧭 Define nav items in one place
  const navItems = [
    { path: "/", label: "Home" },
    { path: "/issue", label: "Issue Book" },
    { path: "/requests", label: "Requests" },
    { path: "/donate", label: "Donate" },
  ];


const sidebarItems = [
  {path: '/dashboard', label: 'Dashboard'},
  {path: '/my-listings', label: 'My Listings'},
  {path: '/books-requested', label: 'Books Requested'},
  {path: '/settings', label: 'Settings'},
  {path: '/help', label: 'Help'},
]

  // 🧵 Refs for nav links
  const navRefs = useRef({});
  navItems.forEach(({ path }) => {
    navRefs.current[path] = navRefs.current[path] || React.createRef();
  });

  // Profile Dropdown State
  const [profileMenuOpen, setProfileMenuOpen] = useState(false);
  const toggleProfileMenu = () => setProfileMenuOpen(!profileMenuOpen);

  // 🔶 Underline position state
  const [underlineStyle, setUnderlineStyle] = useState({ left: 0, width: 0 });

  // 🧠 Update underline on path change
  useEffect(() => {
    const currentRef = navRefs.current[location.pathname];
    if (currentRef?.current) {
      const rect = currentRef.current.getBoundingClientRect();
      const navRect = currentRef.current.parentElement.getBoundingClientRect();
      setUnderlineStyle({
        left: rect.left - navRect.left,
        width: rect.width,
      });
    }
    function handleClickOutSide(e){
      if (dropDownRef.current && !dropDownRef.current.contains(e.target)) {
        setProfileMenuOpen(false);
      }    }
      if (profileMenuOpen)
        document.addEventListener("mousedown", handleClickOutSide);
      else
        document.removeEventListener("mousedown", handleClickOutSide);
    return () => {
      document.removeEventListener("mousedown", handleClickOutSide);
    }
  }, [location.pathname, profileMenuOpen]);

  

  // Sidebar State
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const toggleSidebar = () => setSidebarOpen(!sidebarOpen);

  return (
    <>
      <header className="bg-white dark:bg-zinc-700 dark:text-gray-50 shadow-md h-16 flex items-center justify-between px-6 relative">
        {/* Left: Logo + Search */}
        <div className="flex items-center gap-6 w-1/2">
          <IoMenu
            size={24}
            onClick={toggleSidebar}
            className="cursor-pointer"
          />
          <span className="text-lg font-semibold">LibraryHUB</span>
          <div className="flex items-center bg-gray-200 dark:bg-zinc-600 text-gray-500 dark:text-gray-200 rounded-md px-4 py-2 w-full max-w-md">
            <IoSearch size={20} className="mr-3" />
            <span className="text-sm">Search anything...</span>
          </div>
        </div>

        {/* Center: Nav */}
        <nav className="relative hidden  lg:flex gap-8 h-full items-center">
          {navItems.map(({ path, label }) => (
            <NavLink
              key={path}
              to={path}
              ref={navRefs.current[path]}
              className={({ isActive }) =>
                `text-lg h-full flex items-center transition-colors duration-300 ${
                  isActive ? "text-orange-400 font-medium" : "text-white"
                }`
              }
            >
              {label}
            </NavLink>
          ))}

          {/* 🔶 Dynamic Underline */}
          <span
            className="absolute bottom-0 h-[3px] bg-orange-400 transition-all duration-300"
            style={{
              left: underlineStyle.left,
              width: underlineStyle.width,
            }}
          />
        </nav>

        {/* Right: Profile */}
        <div className="flex items-center gap-2 dark:text-gray-50 hover:bg-gray-100 dark:hover:bg-zinc-600 p-2 rounded-md cursor-pointer">
          <FaRegUser size={22} />
          <span>John Doe</span>
          <IoIosArrowDown size={20} onClick={toggleProfileMenu} />
        </div>

        {/* Profile Dropdown */}
        {profileMenuOpen && (
          <div ref={dropDownRef} className="absolute right-6 top-16 bg-white dark:bg-zinc-700 shadow-lg rounded-md w-48 py-2 z-10">
            <Link to="/profile" className="block px-4 py-2 hover:bg-gray-100 dark:hover:bg-zinc-600">
              My Profile
            </Link>
            <Link to="/settings" className="block px-4 py-2 hover:bg-gray-100 dark:hover:bg-zinc-600">
              Settings
            </Link>
            <Link to="/logout" className="block px-4 py-2 hover:bg-gray-100 dark:hover:bg-zinc-600">
              Logout
            </Link>
          </div>
        )}
      </header>

      <div
        className={`fixed top-0 left-0 w-64 bg-white shadow-lg h-full transform ${
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
                className="text-lg text-gray-700 hover:text-orange-400"
                onClick={() => setSidebarOpen(false)} // Close sidebar on click
              >
                {label}
              </NavLink>
            ))}
          </nav>
        </div>
      </div>
    </>
  );
}

export default Header;
