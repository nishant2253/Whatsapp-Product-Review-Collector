import { useEffect, useState } from "react";
import { fetchReviews } from "./api/review";
import ReviewsTable from "./components/ReviewTable";

function App() {
  const [reviews, setReviews] = useState([]);

  useEffect(() => {
    fetchReviews().then((data) => {
      setReviews(data);
    });
  }, []);

  return (
    <div style={{ padding: "40px" }}>
      <h2>WhatsApp Product Reviews</h2>
      <ReviewsTable reviews={reviews} />
    </div>
  );
}

export default App;
