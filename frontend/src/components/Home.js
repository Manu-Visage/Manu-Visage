import React from "react";
import { useNavigate } from "react-router-dom";
const Button = ({ children, onClick }) => (
  <button className="mt-4 p-2 bg-blue-500 text-white rounded" onClick={onClick}>
    {children}
  </button>
);


const Home = () => {
  const navigate = useNavigate();
  return (
    <div className="flex flex-col items-center justify-center h-screen">
      <h1 className="text-2xl font-bold">Welcome to the Quiz Test</h1>
      <Button className="mt-4 p-2 bg-blue-500 text-white rounded" onClick={() => navigate("/camera")}>
        Start
      </Button>
    </div>
  );
};

export default Home;
