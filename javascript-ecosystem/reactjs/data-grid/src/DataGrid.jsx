import React, { useState, useEffect, useMemo, useCallback } from "react";
import GridRow from "./GridRow";

const DataGrid = () => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);

  // Sorting State
  const [sortConfig, setSortConfig] = useState({ key: null, direction: "asc" });

  // Pagination State
  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 5;

  // Unrelated state to demonstrate React.memo effectiveness
  const [dummyCounter, setDummyCounter] = useState(0);

  // 1. Fetch Dummy Data
  useEffect(() => {
    fetch("https://jsonplaceholder.typicode.com/users")
      .then((response) => response.json())
      .then((json) => {
        console.log("runnning always");

        setData(json);
        setLoading(false);
      });
  }, []);

  // 2. Sorting Logic (Memoized calculation)
  // We use useMemo here so we don't re-sort the array on every render
  // unless data or sortConfig changes.
  const sortedData = useMemo(() => {
    let sortableItems = [...data];
    if (sortConfig.key !== null) {
      sortableItems.sort((a, b) => {
        // Handle nested properties (e.g. company.name) roughly for this demo
        let aValue = a[sortConfig.key];
        let bValue = b[sortConfig.key];

        // Simple check for nested company name for demo purposes
        if (sortConfig.key === "company") {
          aValue = a.company.name;
          bValue = b.company.name;
        }

        if (aValue < bValue) {
          return sortConfig.direction === "ascending" ? -1 : 1;
        }
        if (aValue > bValue) {
          return sortConfig.direction === "ascending" ? 1 : -1;
        }
        return 0;
      });
    }
    return sortableItems;
  }, [data, sortConfig]);

  // 3. Pagination Logic
  const indexOfLastItem = currentPage * itemsPerPage;
  const indexOfFirstItem = indexOfLastItem - itemsPerPage;
  const currentItems = sortedData.slice(indexOfFirstItem, indexOfLastItem);
  const totalPages = Math.ceil(sortedData.length / itemsPerPage);

  // 4. PERFORMANCE: useCallback for Sort Handler
  // This ensures the function reference remains stable across renders
  // unless dependecies change.
  const handleSort = useCallback((key) => {
    setSortConfig((prevConfig) => {
      let direction = "ascending";
      if (prevConfig.key === key && prevConfig.direction === "ascending") {
        direction = "descending";
      }
      return { key, direction };
    });
  }, []);

  if (loading) return <p>Loading data...</p>;

  return (
    <div className="container">
      <h2>React Performance Data Grid</h2>

      {/* Test Area for React.memo */}
      <div className="highlight-box">
        <p>
          <strong>Performance Check:</strong> Click the button below. The "dummy
          counter" state updates, causing the parent <code>DataGrid</code> to
          re-render.
        </p>
        <p>
          However, check the console. You will see <strong>NO</strong>{" "}
          "Rendering Row" logs because <code>GridRow</code> is wrapped in{" "}
          <code>React.memo</code>.
        </p>
        <button onClick={() => setDummyCounter((c) => c + 1)}>
          Update Unrelated State: {dummyCounter}
        </button>
      </div>

      <table>
        <thead>
          <tr>
            <th onClick={() => handleSort("id")}>
              ID{" "}
              {sortConfig.key === "id"
                ? sortConfig.direction === "ascending"
                  ? "▲"
                  : "▼"
                : ""}
            </th>
            <th onClick={() => handleSort("name")}>
              Name{" "}
              {sortConfig.key === "name"
                ? sortConfig.direction === "ascending"
                  ? "▲"
                  : "▼"
                : ""}
            </th>
            <th onClick={() => handleSort("email")}>
              Email{" "}
              {sortConfig.key === "email"
                ? sortConfig.direction === "ascending"
                  ? "▲"
                  : "▼"
                : ""}
            </th>
            <th onClick={() => handleSort("company")}>
              Company{" "}
              {sortConfig.key === "company"
                ? sortConfig.direction === "ascending"
                  ? "▲"
                  : "▼"
                : ""}
            </th>
          </tr>
        </thead>
        <tbody>
          {currentItems.map((user) => (
            <GridRow key={user.id} user={user} />
          ))}
        </tbody>
      </table>

      <div className="pagination">
        <button
          onClick={() => setCurrentPage((prev) => Math.max(prev - 1, 1))}
          disabled={currentPage === 1}
        >
          Previous
        </button>
        <span>
          Page {currentPage} of {totalPages}
        </span>
        <button
          onClick={() =>
            setCurrentPage((prev) => Math.min(prev + 1, totalPages))
          }
          disabled={currentPage === totalPages}
        >
          Next
        </button>
      </div>
    </div>
  );
};

export default DataGrid;
