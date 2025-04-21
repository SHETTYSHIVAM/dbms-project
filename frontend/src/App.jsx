import Home from "./components/Home/Home";
import Header from "./components/Header";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import DashBoard from "./components/Dashboard/DashBoard";
import ManageBooks from "./components/ManageBooks/ManageBooks";
import Login from "./components/Login/Login";
import { ToastContainer } from "react-toastify";
import { AuthProvider } from "./context/AuthContext";
import Profile from "./components/Profile/Profile";
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
        </Routes>
      </AuthProvider>
    </>
  );
}
export default App;
