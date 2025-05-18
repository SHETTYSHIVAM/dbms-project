import {Navigate} from "react-router-dom";
import {useAuth} from "./AuthContext";

const ProtectedRoutes = ({children}) => {
    const {isLoggedIn, user} = useAuth();

    if (!isLoggedIn) {
        return <Navigate to="/login" replace/>;
    }

    return children;
};

export default ProtectedRoutes;
