import React, {useEffect, useRef, useState} from "react";
import {Link, NavLink, useLocation} from "react-router-dom";
import {FaRegUser} from "react-icons/fa";
import {IoIosArrowDown} from "react-icons/io";
import {useAuth} from "../context/AuthContext";

function Header() {
  const location = useLocation();
  const dropDownRef = useRef(null);
  const { isLoggedIn, handleLogout, user } = useAuth();
    const navItems =
        user?.user_type === "admin"
            ? [
                {path: "/", label: "Home"},
                {path: "/requests", label: "Requests"},
                {path: "/issue-books", label: "Issue Book"},
                {path: "/register", label: "Register Users"},
                {path: "/manage-books", label: "Manage Books"},
                {path: "/dashboard", label: "Dashboard"},
            ]
            : [
                {path: "/", label: "Home"},
                {path: "/dashboard", label: "Dashboard"},
            ];

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
    function handleClickOutSide(e) {
      if (dropDownRef.current && !dropDownRef.current.contains(e.target)) {
        setProfileMenuOpen(false);
      }
    }
    if (profileMenuOpen)
      document.addEventListener("mousedown", handleClickOutSide);
    else document.removeEventListener("mousedown", handleClickOutSide);
    return () => {
      document.removeEventListener("mousedown", handleClickOutSide);
    };
  }, [location.pathname, profileMenuOpen]);

  return (
    <>
      <header className="bg-white dark:bg-zinc-800 dark:text-gray-50 shadow-md h-16 flex items-center justify-between px-6 relative">
        {/* Left: Logo + Search */}
        <div className="flex items-center gap-6 w-1/2">
          <span className="text-lg font-semibold">LibraryHUB</span>
        </div>

        {/* Center: Nav */}
        <nav className="relative hidden  lg:flex gap-8 h-full items-center">
          {navItems.map(({ path, label }) => (
            <NavLink
              key={path}
              to={path}
              ref={navRefs.current[path]}
              className={({ isActive }) =>
                `text-lg h-full flex  items-center transition-colors duration-300 ${
                  isActive ? "text-orange-400 font-medium" : "text-gray-500"
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
        {isLoggedIn ? (
          <div className="flex items-center gap-2 dark:text-gray-50 hover:bg-gray-100 dark:hover:bg-zinc-600 p-2 rounded-md cursor-pointer">
            <FaRegUser size={22} />
            <span>{user.username}</span>
            <IoIosArrowDown size={20} onClick={toggleProfileMenu} />
          </div>
        ) : (
          <Link
            to="/login"
            className="bg-orange-400 text-white px-4 py-2 rounded-md transition-colors duration-300 hover:bg-orange-500"
          >
            Login
          </Link>
        )}

        {/* Profile Dropdown */}
        {profileMenuOpen && (
          <div
            ref={dropDownRef}
            className="absolute right-6 top-16 bg-white dark:bg-zinc-800 shadow-lg rounded-md w-48 py-2 z-10"
          >
            <Link
              to="/profile"
              className="block px-4 py-2 hover:bg-gray-100 dark:hover:bg-zinc-600"
            >
              My Profile
            </Link>
            <Link
              to="/settings"
              className="block px-4 py-2 hover:bg-gray-100 dark:hover:bg-zinc-600"
            >
              Settings
            </Link>
            <Link
              onClick={handleLogout}
              className="block px-4 py-2 hover:bg-gray-100 dark:hover:bg-zinc-600"
            >
              Logout
            </Link>
          </div>
        )}
      </header>
    </>
  );
}

export default Header;
