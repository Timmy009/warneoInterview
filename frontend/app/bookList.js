import React, { useEffect, useState } from "react";
import {
  Text,
  View,
  StyleSheet,
  ScrollView,
  ActivityIndicator,
  Pressable,
} from "react-native";
import { useRouter } from "expo-router";
import { LinearGradient } from "expo-linear-gradient";
import Toast from "react-native-toast-message";

const API_URL = "https://25ed-102-88-34-41.ngrok-free.app/books";

export default function BookList() {
  const [loading, setLoading] = useState(false);
  const [books, setBooks] = useState([]);
  const router = useRouter();

  useEffect(() => {
    listBooks();
  }, []);

  const showToast = (type, message) => {
    Toast.show({
      type,
      text2: message,
      position: "top",
    });
  };

  const listBooks = () => {
    setLoading(true);
    fetch(API_URL, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((response) => response.json())
      .then((data) => {
        if (Array.isArray(data)) {
          setBooks(data);
        } else {
          showToast("error", "Invalid response from the server");
        }
      })
      .catch((error) => {
        showToast("error", error.message);
        console.error("Error:", error);
      })
      .finally(() => {
        setLoading(false);
      });
  };

  const navigateToHome = () => {
    router.replace("/"); // Assuming your home page route is "/"
  };

  return (
    <ScrollView style={styles.container}>
      <View style={{ flexDirection: "row", alignItems: "center" }}>
        {loading ? (
          <ActivityIndicator size="large" color="#fff" />
        ) : books.length === 0 ? (
          <Text style={styles.noBooksText}>No books available</Text>
        ) : (
          <View>
            {books.map((book) => (
              <View key={book.id} style={styles.bookItem}>
                <Text style={styles.title}>{book.title}</Text>
                <Text style={styles.author}>Author: {book.author}</Text>
              </View>
            ))}
          </View>
        )}
      </View>
      <Pressable onPress={navigateToHome}>
        <LinearGradient
          colors={["#DF00BC", "#9C00E4"]}
          start={[0, 0]}
          end={[1, 0]}
          style={[styles.button, { marginTop: 20 }]}
        >
          <Text style={{ color: "#fff", fontWeight: "600" }}>Go Home</Text>
        </LinearGradient>
      </Pressable>
      <Toast />
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#000",
    paddingTop: 40,
    paddingHorizontal: 15,
  },
  bookItem: {
    marginBottom: 20,
  },
  title: {
    color: "#fff",
    fontSize: 20,
    fontWeight: "bold",
  },
  author: {
    color: "#888888",
    fontSize: 14,
  },
  noBooksText: {
    color: "#fff",
    fontSize: 18,
    textAlign: "center",
    marginTop: 20,
  },
  button: {
    paddingVertical: 15,
    justifyContent: "center",
    alignItems: "center",
    backgroundColor: "#DF00BC",
    borderRadius: 15,
  },
});
