import React, { useState, useRef } from "react";
import Webcam from "react-webcam";
import QuizPage from "./QuizPage";

const Button = ({ children, onClick }) => (
  <button className="mt-4 p-2 bg-blue-500 text-white rounded" onClick={onClick}>
    {children}
  </button>
);
const CameraPage = () => {
  const [capturedImage, setCapturedImage] = useState(null);
  const webcamRef = useRef(null);

  const capturePhoto = async () => {
    const imageSrc = webcamRef.current.getScreenshot();
    setCapturedImage(imageSrc);

    // Send image to backend
    await fetch("http://localhost:5000/capture", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ image: imageSrc })
    });
  };

  return (
    <div className="flex flex-col items-center justify-center h-screen">
      {!capturedImage ? (
        <>
          <Webcam ref={webcamRef} screenshotFormat="image/png" className="w-96 h-72 border-2" />
          <Button className="mt-4 bg-green-500 text-white p-2 rounded" onClick={capturePhoto}>
            Capture Photo
          </Button>
        </>
      ) : (
        <>
          <img src={capturedImage} alt="Captured" className="absolute top-4 right-4 w-32 h-32 border-2" />
          <QuizPage />
        </>
      )}
    </div>
  );
};

export default CameraPage;