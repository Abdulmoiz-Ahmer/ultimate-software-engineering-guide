import React from "react";

const GridRow = ({ user }) => {
  // Logic check: This log will appear ONLY when this specific row actually renders.
  // If we update a parent state unrelated to this row, this log should NOT fire.
  console.log(`Rendering Row: ${user.id}`);

  return (
    <tr>
      <td>{user.id}</td>
      <td>{user.name}</td>
      <td>{user.email}</td>
      <td>{user.company.name}</td>
    </tr>
  );
};

// PERFORMANCE: Wrap in React.memo
// This prevents the row from re-rendering if the parent re-renders
// but the 'user' prop remains exactly the same.
export default React.memo(GridRow);
