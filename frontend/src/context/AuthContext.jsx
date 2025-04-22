import React, { createContext, useContext, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

// 1. Create the context
const AuthContext = createContext();

// 2. AuthProvider component
export const AuthProvider = ({ children }) => {
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);
    const navigate = useNavigate();

    useEffect(() => {
        const loadAuthFromStorage = () => {
            try {
                const accessToken = localStorage.getItem("accessToken");
                const refreshToken = localStorage.getItem("refreshToken");
                const userData = localStorage.getItem("user");

                if (accessToken && refreshToken && userData) {
                    setUser(JSON.parse(userData));
                    setIsLoggedIn(true);
                } else {
                    clearAuthState();
                }
            } catch (err) {
                console.error("Auth loading failed:", err);
                clearAuthState();
            } finally {
                setLoading(false);
            }
        };

        loadAuthFromStorage();
    }, []);

    const clearAuthState = () => {
        setIsLoggedIn(false);
        setUser(null);
        localStorage.removeItem("accessToken");
        localStorage.removeItem("refreshToken");
        localStorage.removeItem("user");
    };

    const handleLogin = (userData) => {
        setIsLoggedIn(true);
        setUser(userData);
        localStorage.setItem("accessToken", userData.accessToken);
        localStorage.setItem("refreshToken", userData.refreshToken);
        localStorage.setItem("user", JSON.stringify(userData));
        navigate("/");
    };

    const handleLogout = () => {
        clearAuthState();
        navigate("/login");
    };

    const value = {
        isLoggedIn,
        user,
        loading,
        handleLogin,
        handleLogout,
    };

    return (
        <AuthContext.Provider value={value}>
            {children}
        </AuthContext.Provider>
    );
};



export const useAuth = () => {
    return useContext(AuthContext);
};
