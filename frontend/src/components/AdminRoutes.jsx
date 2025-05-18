import {useAuth} from "../context/AuthContext";

const AdminRoutes = ({children}) => {
    const {isLoggedIn, user} = useAuth();
    console.log("AdminRoutes", isLoggedIn, user);

    if (!isLoggedIn || user.user_type !== "admin") {
        return <h1>You have no permission to access this page</h1>;
    }

    return children;
};

export default AdminRoutes;
