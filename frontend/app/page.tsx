"use client";

import React, { useEffect, useState } from "react";

type Report = {
  ticker: string;
  date: string; // YYYY-MM-DD
  when?: string;
  issuer_name?: string;
  rank?: number;
  value?: number;
  growth?: number;
  momentum?: number;
  vgm?: number;
  eps_hist?: number;
};

type Grouped = {
  date: string;
  items: Report[];
};

export default function EarningsCalendarPage() {
  const [groups, setGroups] = useState<Grouped[]>([]);
  const [loading, setLoading] = useState(true);
  const [currentDateIndex, setCurrentDateIndex] = useState(0);
  const [expanded, setExpanded] = useState<Record<string, boolean>>({});

  useEffect(() => {
    let mounted = true;
    async function load() {
      setLoading(true);
      try {
        const res = await fetch("/api");
        const json = await res.json();
        const reports: Report[] = json.earningsReports ?? json;
        const map = new Map<string, Report[]>();
        for (const r of reports) {
          const d = r.date;
          if (!map.has(d)) map.set(d, []);
          map.get(d)!.push(r);
        }
        const grouped: Grouped[] = Array.from(map.entries())
          .sort((a, b) => a[0].localeCompare(b[0]))
          .map(([date, items]) => ({ date, items }));
        if (mounted) setGroups(grouped);
      } catch (e) {
        console.error("Failed to load earnings:", e);
        if (mounted) setGroups([]);
      } finally {
        if (mounted) setLoading(false);
      }
    }
    load();
    return () => {
      mounted = false;
    };
  }, []);

  if (loading) return <div style={{ padding: 20 }}>Loading earnings...</div>;
  if (!groups.length) return <div style={{ padding: 20 }}>No upcoming earnings found.</div>;

  const currentGroup = groups[currentDateIndex];
  const beforeMarket = currentGroup.items.filter((r) => r.when?.toLowerCase() === "before market" || r.when?.toLowerCase().includes("before"));
  const afterMarket = currentGroup.items.filter((r) => r.when?.toLowerCase() === "after market" || r.when?.toLowerCase().includes("after"));
  const unknown = currentGroup.items.filter((r) => !r.when || (!r.when.toLowerCase().includes("before") && !r.when.toLowerCase().includes("after")));

  const goToPrev = () => setCurrentDateIndex(Math.max(0, currentDateIndex - 1));
  const goToNext = () => setCurrentDateIndex(Math.min(groups.length - 1, currentDateIndex + 1));

  const formatDate = (dateStr: string) => {
    return new Date(dateStr + "T00:00:00").toLocaleDateString("en-US", {
      weekday: "long",
      month: "2-digit",
      day: "2-digit",
      year: "numeric",
    });
  };

  const renderCards = (items: Report[]) => (
    <div style={{ display: "flex", gap: 12, flexWrap: "wrap" }}>
      {items.map((r) => {
        const key = `${currentGroup.date}-${r.ticker}`;
        return (
          <button
            key={key}
            onClick={() => setExpanded((s) => ({ ...s, [key]: !s[key] }))}
            style={{
              width: 220,
              textAlign: "left",
              padding: 12,
              borderRadius: 8,
              border: "1px solid #e6edf3",
              background: "#fff",
              cursor: "pointer",
              boxShadow: "0 1px 2px rgba(0,0,0,0.03)",
            }}
            aria-expanded={!!expanded[key]}
          >
            <div style={{ display: "flex", alignItems: "center" }}>
              <div style={{ fontWeight: 700, color: "#464647" }}>{r.ticker}</div>
            </div>
            <div style={{ marginTop: 8, fontSize: 13, color: "#374151" }}>{r.issuer_name ?? ""}</div>
            {expanded[key] && (
              <div style={{ marginTop: 8, fontSize: 13, color: "#111827" }}>
                <div><strong>Ticker:</strong> {r.ticker}</div>
                <div><strong>Date:</strong> {r.date}</div>
                <div><strong>Rank:</strong> {r.rank ?? "N/A"}</div>
                <div><strong>Value:</strong> {r.value ?? "N/A"}</div>
                <div><strong>Growth:</strong> {r.growth ?? "N/A"}</div>
                <div><strong>Momentum:</strong> {r.momentum ?? "N/A"}</div>
                <div><strong>VGM:</strong> {r.vgm ?? "N/A"}</div>
                <div><strong>prev eps:</strong> {r.eps_hist ?? "N/A"}</div>
              </div>
            )}
          </button>
        );
      })}
    </div>
  );

  return (
    <div style={{ padding: 20, fontFamily: "system-ui, Arial, sans-serif", background: "#f6f4f3", minHeight: "100vh" }}>
      <h1 style={{ marginBottom: 16, color: "#111827" }}>Earnings Calendar</h1>

      {/* Navigation */}
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 20 }}>
        <button
          onClick={goToPrev}
          disabled={currentDateIndex === 0}
          style={{
            padding: "8px 16px",
            borderRadius: 4,
            border: "1px solid #dcdcdc",
            background: currentDateIndex === 0 ? "#f5f5f5" : "#fff",
            cursor: currentDateIndex === 0 ? "not-allowed" : "pointer",
            color: currentDateIndex === 0 ? "#999" : "#000",
          }}
        >
          ← Previous
        </button>

        <div style={{ fontSize: 18, fontWeight: 600, color: "#111827" }}>
          {formatDate(currentGroup.date)}
        </div>

        <button
          onClick={goToNext}
          disabled={currentDateIndex === groups.length - 1}
          style={{
            padding: "8px 16px",
            borderRadius: 4,
            border: "1px solid #dcdcdc",
            background: currentDateIndex === groups.length - 1 ? "#f5f5f5" : "#fff",
            cursor: currentDateIndex === groups.length - 1 ? "not-allowed" : "pointer",
            color: currentDateIndex === groups.length - 1 ? "#999" : "#000",
          }}
        >
          Next →
        </button>
      </div>

      {/* Two-column layout: Before (left) and After (right) */}
      {(beforeMarket.length > 0 || afterMarket.length > 0) && (
        <div style={{ display: "flex", gap: 48, alignItems: "flex-start", marginBottom: 20 }}>
          <section style={{ flex: 1 }}>
            <h2 style={{ fontSize: 16, fontWeight: 600, marginBottom: 12, color: "#000000" }}>
              Before Market ({beforeMarket.length})
            </h2>
            {beforeMarket.length > 0 ? renderCards(beforeMarket) : <div style={{ color: "#888" }}>No before-market items.</div>}
          </section>

          <section style={{ flex: 1 }}>
            <h2 style={{ fontSize: 16, fontWeight: 600, marginBottom: 12, color: "#000000", textAlign: "right" }}>
              After Market ({afterMarket.length})
            </h2>
            <div style={{ display: "flex", justifyContent: "flex-end" }}>
              {afterMarket.length > 0 ? renderCards(afterMarket) : <div style={{ color: "#888" }}>No after-market items.</div>}
            </div>
          </section>
        </div>
      )}

      {/* Unknown Time */}
      {unknown.length > 0 && (
        <section>
          <h2 style={{ fontSize: 16, fontWeight: 600, marginBottom: 12, color: "#374151" }}>
            Time Not Specified ({unknown.length})
          </h2>
          {renderCards(unknown)}
        </section>
      )}

      {currentGroup.items.length === 0 && (
        <div style={{ color: "#888", fontSize: 14 }}>No earnings scheduled for this day.</div>
      )}
    </div>
  );
}
