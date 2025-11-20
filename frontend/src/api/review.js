export async function fetchReviews() {
  const res = await fetch("http://localhost:8000/api/reviews");
  return res.json();
}
