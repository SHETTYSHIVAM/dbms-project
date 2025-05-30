import {useAuth} from "../context/AuthContext";

const AdminRoutes = ({children}) => {
    const {isLoggedIn, user} = useAuth();

    if (!isLoggedIn || user.user_type !== "admin") {
        return (
            <div className="flex items-center justify-center min-h-screen bg-gray-50 dark:bg-zinc-800">
                <div className="bg-white dark:bg-zinc-700 p-6 rounded shadow-md">
                    <h2 className="text-2xl font-semibold text-gray-700 dark:text-gray-200">
                        Access Denied
                    </h2>
                    <p className="mt-4 text-gray-600 dark:text-gray-400">
                        You do not have permission to access this page.
                    </p>
                </div>
            </div>
        );
    }

    return children;
};

export default AdminRoutes;
