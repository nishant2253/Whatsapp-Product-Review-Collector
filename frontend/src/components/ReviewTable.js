import React from "react";

function ReviewsTable({ reviews }) {
  return (
    <table
      style={{ width: "100%", borderCollapse: "collapse", marginTop: "20px" }}
    >
      <thead>
        <tr>
          <th>User</th>
          <th>Product</th>
          <th>Review</th>
          <th>Timestamp</th>
        </tr>
      </thead>
      <tbody>
        {reviews.map((r) => (
          <tr key={r.id}>
            <td>{r.user_name}</td>
            <td>{r.product_name}</td>
            <td>{r.product_review}</td>
            <td>{new Date(r.created_at).toLocaleString()}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}

export default ReviewsTable;
