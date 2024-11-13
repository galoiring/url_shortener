import React, { useState, useEffect } from "react";
import { Button } from "./ui/button";
import { Input } from "./ui/input";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  CardDescription,
} from "./ui/card";
import {
  AlertCircle,
  CheckCircle,
  Copy,
  LinkIcon,
  ExternalLink,
  History,
} from "lucide-react";
import { Alert, AlertDescription, AlertTitle } from "./ui/alert";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "./ui/table";
import { Badge } from "./ui/badge";

const URLShortener = () => {
  const [url, setUrl] = useState("");
  const [shortUrl, setShortUrl] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [history, setHistory] = useState([]);
  const [isLoadingHistory, setIsLoadingHistory] = useState(true);

  const validateUrl = (url) => {
    if (!/^https?:\/\//i.test(url)) {
      url = "http://" + url;
    }
    try {
      new URL(url);
      return url;
    } catch {
      return false;
    }
  };

  const fetchHistory = async () => {
    try {
      const response = await fetch("/api/urls/");
      const data = await response.json();
      setHistory(data);
    } catch (error) {
      console.error("Failed to fetch history:", error);
    } finally {
      setIsLoadingHistory(false);
    }
  };

  useEffect(() => {
    fetchHistory();
  }, []);

  const handleShorten = async () => {
    const validUrl = validateUrl(url);
    if (!validUrl) {
      setError("Please enter a valid URL");
      return;
    }
    setIsLoading(true);
    setError("");
    setSuccess("");
    try {
      const response = await fetch("/api/create/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCookie("csrftoken"),
        },
        body: JSON.stringify({ url: validUrl }),
      });
      const data = await response.json();
      if (response.ok) {
        setShortUrl(window.location.origin + "/" + data.short_url);
        setSuccess("URL shortened successfully!");
        fetchHistory();
      } else {
        throw new Error(data.error || "Failed to shorten URL");
      }
    } catch (error) {
      setError(error.message);
    } finally {
      setIsLoading(false);
    }
  };

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(shortUrl);
      setSuccess("Copied to clipboard!");
      setTimeout(() => setSuccess(""), 2000);
    } catch (err) {
      setError("Failed to copy to clipboard");
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString("en-US", {
      month: "short",
      day: "numeric",
      year: "numeric",
    });
  };

  const getCookie = (name) => {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  };

  return (
    <div className='min-h-screen bg-gradient-to-b from-gray-50 to-gray-100 p-4 md:p-8'>
      <div className='max-w-4xl mx-auto space-y-8'>
        <Card className='w-full'>
          <CardHeader>
            <CardTitle className='text-2xl font-bold text-center text-primary'>
              URL Shortener
            </CardTitle>
            <CardDescription className='text-center'>
              Shorten your links with just one click
            </CardDescription>
          </CardHeader>
          <CardContent className='space-y-4'>
            <div className='flex flex-col md:flex-row items-center gap-2'>
              <Input
                type='text'
                placeholder='Enter your URL here (e.g., google.com)'
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                className='flex-grow'
              />
              <Button
                onClick={handleShorten}
                disabled={isLoading}
                className='w-full md:w-auto'
              >
                {isLoading ? (
                  <>Loading...</>
                ) : (
                  <>
                    <LinkIcon className='mr-2 h-4 w-4' />
                    Shorten
                  </>
                )}
              </Button>
            </div>

            {shortUrl && (
              <div className='flex items-center justify-between bg-gray-50 p-3 rounded-md border'>
                <a
                  href={shortUrl}
                  target='_blank'
                  rel='noopener noreferrer'
                  className='text-primary hover:underline truncate flex items-center gap-2'
                >
                  {shortUrl}
                  <ExternalLink className='h-4 w-4' />
                </a>
                <Button variant='ghost' size='icon' onClick={handleCopy}>
                  <Copy className='h-4 w-4' />
                </Button>
              </div>
            )}

            {error && (
              <Alert variant='destructive'>
                <AlertCircle className='h-4 w-4' />
                <AlertTitle>Error</AlertTitle>
                <AlertDescription>{error}</AlertDescription>
              </Alert>
            )}

            {success && (
              <Alert
                variant='default'
                className='bg-green-50 text-green-800 border-green-200'
              >
                <CheckCircle className='h-4 w-4' />
                <AlertTitle>Success</AlertTitle>
                <AlertDescription>{success}</AlertDescription>
              </Alert>
            )}
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className='text-xl font-semibold flex items-center gap-2'>
              <History className='h-5 w-5' />
              Recent Links
            </CardTitle>
          </CardHeader>
          <CardContent>
            {isLoadingHistory ? (
              <div className='text-center py-4 text-gray-500'>
                Loading history...
              </div>
            ) : (
              <div className='rounded-md border'>
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Original URL</TableHead>
                      <TableHead>Short URL</TableHead>
                      <TableHead>Hits</TableHead>
                      <TableHead>Created</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {history.length > 0 ? (
                      history.map((item, index) => (
                        <TableRow key={index}>
                          <TableCell className='max-w-[200px] truncate'>
                            <a
                              href={item.original_url}
                              target='_blank'
                              rel='noopener noreferrer'
                              className='text-primary hover:underline flex items-center gap-1'
                            >
                              {item.original_url}
                              <ExternalLink className='h-3 w-3' />
                            </a>
                          </TableCell>
                          <TableCell>
                            <a
                              href={item.short_url}
                              target='_blank'
                              rel='noopener noreferrer'
                              className='text-primary hover:underline flex items-center gap-1'
                            >
                              {item.short_url}
                              <ExternalLink className='h-3 w-3' />
                            </a>
                          </TableCell>
                          <TableCell>
                            <Badge variant='secondary'>
                              {item.hits} clicks
                            </Badge>
                          </TableCell>
                          <TableCell className='text-gray-500'>
                            {formatDate(item.created_at)}
                          </TableCell>
                        </TableRow>
                      ))
                    ) : (
                      <TableRow>
                        <TableCell
                          colSpan={4}
                          className='text-center py-8 text-gray-500'
                        >
                          No shortened URLs yet. Create your first one above!
                        </TableCell>
                      </TableRow>
                    )}
                  </TableBody>
                </Table>
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default URLShortener;
