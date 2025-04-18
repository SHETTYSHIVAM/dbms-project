import Home from "./components/Home/Home";
import Header from "./components/Header";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import DashBoard from "./components/Dashboard/DashBoard";
function App() {
  return (
    <>
      <Header />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/dashboard" element={<DashBoard/>} />
      </Routes>
    </>
  );
}
export default App;
