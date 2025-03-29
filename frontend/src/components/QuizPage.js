import React, { useState } from "react";
const Button = ({ children, onClick }) => (
  <button className="mt-4 p-2 bg-blue-500 text-white rounded" onClick={onClick}>
    {children}
  </button>
);


const QuizPage = () => {
  const questions = [
    { id: 1, question: "What is 2 + 2?", options: ["3", "4", "5"], answer: "4" },
    { id: 2, question: "What is the capital of France?", options: ["Berlin", "Paris", "Madrid"], answer: "Paris" }
  ];

  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [selectedAnswer, setSelectedAnswer] = useState(null);
  const [score, setScore] = useState(0);

  const handleNext = () => {
    if (selectedAnswer === questions[currentQuestion].answer) {
      setScore(score + 1);
    }
    if (currentQuestion < questions.length - 1) {
      setCurrentQuestion(currentQuestion + 1);
      setSelectedAnswer(null);
    } else {
      alert(`Quiz Completed! Your Score: ${score + (selectedAnswer === questions[currentQuestion].answer ? 1 : 0)}`);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center mt-20">
      <h2 className="text-xl font-bold">{questions[currentQuestion].question}</h2>
      {questions[currentQuestion].options.map((option, index) => (
        <Button
          key={index}
          className={`mt-2 p-2 rounded ${selectedAnswer === option ? "bg-blue-500 text-white" : "bg-gray-200"}`}
          onClick={() => setSelectedAnswer(option)}
        >
          {option}
        </Button>
      ))}
      <Button className="mt-4 bg-green-500 text-white p-2 rounded" onClick={handleNext}>
        Next
      </Button>
    </div>
  );
};

export default QuizPage;