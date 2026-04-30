import tkinter as tk
from tkinter import messagebox
import heapq

class DijkstraApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dijkstra Shortest Path (GUI)")
        self.root.geometry("550x600")

        self.graph = {}

        # Title
        tk.Label(root, text="Dijkstra Shortest Path", font=("Arial", 16, "bold")).pack(pady=10)

        # Input Frame
        frame = tk.Frame(root)
        frame.pack(pady=10)

        tk.Label(frame, text="From Node:").grid(row=0, column=0)
        self.from_entry = tk.Entry(frame)
        self.from_entry.grid(row=0, column=1)

        tk.Label(frame, text="To Node:").grid(row=1, column=0)
        self.to_entry = tk.Entry(frame)
        self.to_entry.grid(row=1, column=1)

        tk.Label(frame, text="Weight:").grid(row=2, column=0)
        self.weight_entry = tk.Entry(frame)
        self.weight_entry.grid(row=2, column=1)

        # Buttons
        tk.Button(root, text="Add Edge", command=self.add_edge).pack(pady=5)
        tk.Button(root, text="Find Shortest Path", command=self.find_path).pack(pady=5)
        tk.Button(root, text="Clear", command=self.clear).pack(pady=5)

        # Listbox to show edges
        self.listbox = tk.Listbox(root, width=50, height=10)
        self.listbox.pack(pady=10)

        # Start/End nodes
        tk.Label(root, text="Start Node:").pack()
        self.start_entry = tk.Entry(root)
        self.start_entry.pack()

        tk.Label(root, text="End Node:").pack()
        self.end_entry = tk.Entry(root)
        self.end_entry.pack()

        # Result Label
        self.result_label = tk.Label(root, text="", fg="blue", wraplength=400)
        self.result_label.pack(pady=15)

    def add_edge(self):
        try:
            u = self.from_entry.get()
            v = self.to_entry.get()
            w = int(self.weight_entry.get())

            if not u or not v or w <= 0:
                messagebox.showerror("Error", "Invalid input")
                return

            if u not in self.graph:
                self.graph[u] = []
            if v not in self.graph:
                self.graph[v] = []

            self.graph[u].append((v, w))
            self.graph[v].append((u, w))  # Undirected graph

            self.listbox.insert(tk.END, f"{u} ↔ {v} (Weight: {w})")

            self.from_entry.delete(0, tk.END)
            self.to_entry.delete(0, tk.END)
            self.weight_entry.delete(0, tk.END)

        except ValueError:
            messagebox.showerror("Error", "Enter valid weight")

    def dijkstra(self, start):
        dist = {node: float('inf') for node in self.graph}
        dist[start] = 0
        prev = {}

        pq = [(0, start)]

        while pq:
            current_dist, node = heapq.heappop(pq)

            for neighbor, weight in self.graph[node]:
                new_dist = current_dist + weight

                if new_dist < dist[neighbor]:
                    dist[neighbor] = new_dist
                    prev[neighbor] = node
                    heapq.heappush(pq, (new_dist, neighbor))

        return dist, prev

    def find_path(self):
        start = self.start_entry.get()
        end = self.end_entry.get()

        if start not in self.graph or end not in self.graph:
            messagebox.showerror("Error", "Invalid start or end node")
            return

        dist, prev = self.dijkstra(start)

        path = []
        current = end

        while current in prev:
            path.append(current)
            current = prev[current]
        path.append(start)
        path.reverse()

        result = f"Shortest Distance: {dist[end]}\nPath: {' → '.join(path)}"
        self.result_label.config(text=result)

    def clear(self):
        self.graph.clear()
        self.listbox.delete(0, tk.END)
        self.result_label.config(text="")
        self.start_entry.delete(0, tk.END)
        self.end_entry.delete(0, tk.END)


# Run App
if __name__ == "__main__":
    root = tk.Tk()
    app = DijkstraApp(root)
    root.mainloop()