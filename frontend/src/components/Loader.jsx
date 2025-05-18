import React from "react";

const Loader = () => {
    return (
        <div className="flex justify-center items-center h-screen bg-white">
            <div className="w-16 h-16 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"/>
        </div>
    );
};

export default Loader;
