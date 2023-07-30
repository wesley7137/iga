import Image from "next/image";
import { use, useState, useEffect } from "react";
import { Inter } from "next/font/google";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { PlayOutline, StopOutline } from "@carbon/icons-react";
import KnowledgeGraph from "@/components/Knowledge";
import { Chart } from "react-google-charts";

const inter = Inter({ subsets: ["latin"] });

export default function Home() {
  const [tab, setTab] = useState("dashboard");

  const [socket, setSocket] = useState<WebSocket | null>(null);
  const [isStarted, setIsStarted] = useState(false);

  useEffect(() => {
    const newSocket = new WebSocket("ws://localhost:5001/data");
    setSocket(newSocket);

    newSocket.onopen = () => {
      console.log("connected");
    };

    newSocket.onmessage = (event) => {
      console.log("data from the back end: ", event.data);
    };

    newSocket.onclose = () => {
      console.log("user disconnected");
    };

    return () => {
      newSocket.close();
    };
  }, []);

  const handleStart = () => {
    if (socket) {
      socket.send(JSON.stringify({ action: "start" }));
      setIsStarted(true);
    }
  };

  const handleStop = () => {
    if (socket) {
      socket.send(JSON.stringify({ action: "stop" }));
      setIsStarted(false);
    }
  };

  const columns = [
    { type: "string", id: "Title" },
    { type: "date", id: "Start" },
    { type: "date", id: "End" },
  ];

  //unified data format:
  // msgId
  // msgType: enum
  // timeStart: Date
  // timeEnd: Date
  // msgTitle?: string
  // msgContent?: string
  // graphParent?: string

  const [data, setData] = useState([
    {
      id: 0,
      type: "goal",
      timeStart: new Date(2021, 1, 1),
      timeEnd: new Date(2021, 1, 2),
      title: "Learn more about web development",
    },
    {
      id: 1,
      type: "task",
      timeStart: new Date(2021, 1, 2),
      timeEnd: new Date(2021, 1, 5),
      title: "Search(google, How to learn Next.js)",
      content: "",
    },
    {
      id: 2,
      type: "knowledge",
      timeStart: new Date(2021, 1, 5),
      timeEnd: new Date(2021, 1, 7),
      title: "Next.js Website",
      content: "A summary of Next.js",
    },
    {
      id: 3,
      type: "knowledge",
      timeStart: new Date(2021, 1, 7),
      timeEnd: new Date(2021, 1, 12),
      title: "Next.js blog",
      content: "A summary of Next.js from the blog",
      graphParent: 2,
    },
    {
      id: 4,
      type: "knowledge",
      timeStart: new Date(2021, 1, 12),
      timeEnd: new Date(2021, 1, 13),
      title: "Next.js docs",
      content: "A summary of Next.js from the docs",
      graphParent: 2,
    },
    {
      id: 5,
      type: "skill",
      timeStart: new Date(2021, 1, 13),
      timeEnd: new Date(2021, 1, 15),
      title: "Use next.js CLI",
      content: "Next CLI Summarized Instructions",
    },
  ]);

  const graphData = [
    columns,
    ...data.map((d) => [d.title, d.timeStart, d.timeEnd]),
  ];

  const nodes = data
    .filter((d) => d.type === "knowledge")
    .map((data, i) => ({
      id: data.id,
      index: i,
      content: data.content, // Example content
      title: data.title, // Example title
    }));

  const links = data
    .filter((d) => d.type === "knowledge" && d.graphParent != null)
    .map((d) => ({
      source: d.id,
      target: d.graphParent!,
    }));

  const [graph, setGraph] = useState({
    nodes: nodes,
    links: links,
  });

  return (
    <main
      className={`flex min-h-screen min-w-screen h-screen flex-col items-center justify-between ${inter.className} overflow-hidden`}
    >
      <div className="z-10 h-fit w-full items-center justify-between font-mono text-sm border-b border-gray-400">
        <div className="left-0 top-0 flex w-full justify-center border-b border-gray-300 bg-zinc-300 py-3 backdrop-blur-2xl">
          <div className="w-fill flex items-center justify-center gap-5 w-full">
            IGA - An Impressively General Agent
            <div className="px-2 py-1 rounded bg-slate-800 text-white text-xs">
              Built with Claude-2
            </div>
          </div>
        </div>
      </div>
      <div className="w-full h-full grow p-8 pt-16 bg-slate-50 flex font-mono overflow-hidden">
        <Tabs
          defaultValue="dashboard"
          className="grow flex flex-col gap-2 overflow-hidden"
          onValueChange={(select) => setTab(select)}
          value={tab}
        >
          <div className="flex w-full justify-between items-center">
            <div className="flex items-center gap-4">
              {!isStarted ? (
                <button
                  className="rounded bg-slate-700 transition text-white p-2 text-xs hover:bg-green-500"
                  onClick={handleStart}
                >
                  <PlayOutline className="w-6 h-6" />
                </button>
              ) : (
                <button
                  className="rounded bg-slate-700 transition text-white p-2 text-xs hover:bg-red-500"
                  onClick={handleStop}
                >
                  <StopOutline className="w-6 h-6" />
                </button>
              )}
              <h1 className="text-3xl text-gray-700 flex items-center">
                {tab.toLocaleUpperCase()}
              </h1>
            </div>
            <TabsList className="grid grid-cols-4 rounded border flex">
              <TabsTrigger value="dashboard">Dashboard</TabsTrigger>
              <TabsTrigger value="timeline">Timeline</TabsTrigger>
              <TabsTrigger value="knowledge">Knowledge</TabsTrigger>
              <TabsTrigger value="skills">Skills</TabsTrigger>
            </TabsList>
          </div>
          <TabsContent value="dashboard" className="h-full w-full">
            <div className="flex flex-col w-full h-full gap-4">
              <div className="flex gap-4 w-full">
                <Card className="w-full h-40">
                  <CardHeader>
                    <CardTitle>Macro Goal</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-2">
                    <div className="space-y-1"> {data[0].title}</div>
                  </CardContent>
                </Card>
                <Card className="w-full h-40">
                  <CardHeader>
                    <CardTitle>Current Goal</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-2">
                    {data[data.length - 1].title}
                  </CardContent>
                </Card>
              </div>
              <Card className="w-full h-full overflow-hidden flex flex-col">
                <CardHeader>
                  <CardTitle>Action Feed</CardTitle>
                </CardHeader>
                <CardContent className="h-0 grow flex flex-col overflow-y-scroll mb-4">
                  <div className="grow">
                    {data.map((data, i) => (
                      <div
                        key={i}
                        className="flex flex-col gap-2 my-2 h-fit text-xs"
                      >
                        {JSON.stringify(data)}
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>
          <TabsContent value="timeline" className="h-full w-full">
            <Card className="h-full w-full">
              <CardContent className="w-full h-full grow p-4 flex items-center justify-center">
                <Chart
                  chartType="Timeline"
                  data={graphData}
                  width="100%"
                  height="100%"
                />
              </CardContent>
            </Card>
          </TabsContent>
          <TabsContent value="knowledge" className="h-full w-full">
            <Card className="h-full w-full">
              <CardContent className="w-full h-full grow p-4">
                <KnowledgeGraph graph={graph} />
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="skills" className="h-full w-full overflow-scroll">
            {data
              .filter((d) => d.type === "skill")
              .map((skill, i) => (
                <Card key={i} className="my-2">
                  <CardHeader>
                    <CardTitle>{skill.title}</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="text-sm">{skill.content}</div>
                  </CardContent>
                </Card>
              ))}
          </TabsContent>
        </Tabs>
      </div>
    </main>
  );
}
