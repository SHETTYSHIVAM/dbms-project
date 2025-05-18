import Home from "./components/Home/Home";
import Header from "./components/Header";
import {Route, Routes} from "react-router-dom";
import DashBoard from "./components/Dashboard/DashBoard";
import ManageBooks from "./components/ManageBooks/ManageBooks";
import Login from "./components/Login/Login";
import {ToastContainer} from "react-toastify";
import {AuthProvider} from "./context/AuthContext";
import Profile from "./components/Profile/Profile";
import ViewBook from "./components/ViewBook/ViewBook";
import AdminRoutes from "./components/AdminRoutes";
import AdminRequests from "./components/AdminRequests/AdminRequests";

function App() {
  return (
    <>
      <AuthProvider>
        <Header />
        <ToastContainer />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/dashboard" element={<DashBoard />} />
          <Route path="/manage-books" element={<ManageBooks />} />
          <Route path="/login" element={<Login />} />
          <Route path="/profile" element={<Profile />} />
            <Route path="/books/:id" element={<ViewBook/>}/>
            <Route
                path="/requests"
                element={
                    <AdminRoutes>
                        <AdminRequests/>
                    </AdminRoutes>
                }
            />

          <Route path="*" element={<h1>404 Not Found</h1>} />
        </Routes>
      </AuthProvider>
    </>
  );
}
export default App;
