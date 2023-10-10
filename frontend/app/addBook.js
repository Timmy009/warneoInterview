import React, { useState } from "react";
import {
  Text,
  View,
  TextInput,
  StyleSheet,
  ScrollView,
  ActivityIndicator,
  Pressable,
} from "react-native";
import { useForm, Controller } from "react-hook-form";
import { Link, useRouter } from "expo-router";
import AsyncStorage from "@react-native-async-storage/async-storage";
import { StatusBar } from "react-native";
import { LinearGradient } from "expo-linear-gradient";
import Toast from "react-native-toast-message";

const API_URL = "https://25ed-102-88-34-41.ngrok-free.app/book/add";

export default function AddBook() {
  const [loading, setLoading] = useState(false);
  const {
    control,
    handleSubmit,
    formState: { errors },
  } = useForm({
    defaultValues: {
      title: "",
      author: "",
    },
  });
  const router = useRouter();

  const showToast = (type, message) => {
    Toast.show({
      type,
      text2: message,
      position: "top",
    });
  };

  const onSubmit = (reqdata) => {
    setLoading(true);
    fetch(API_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(reqdata),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.message.includes("Book added successfully")) {
          showToast("success", "Book added successfully");
          router.replace("/bookList");
        } else {
          showToast("error", data.message);
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

  return (
    <>
      <StatusBar />
      <ScrollView style={styles.container}>
        <Text style={styles.title}>ADD BOOK</Text>
        <Text style={styles.smallText}>Enter the book details to add</Text>
        <View
          style={{
            marginTop: 15,
            marginBottom: 40,
            flexDirection: "row",
            justifyContent: "space-between",
          }}
        ></View>
        <Text style={[styles.label, { marginBottom: 10, marginLeft: 7 }]}>
          Title
        </Text>
        <View style={{ position: "relative" }}>
          <Controller
            control={control}
            rules={{
              required: true,
            }}
            render={({ field: { onChange, onBlur, value } }) => (
              <TextInput
                placeholder="Enter the title"
                onBlur={onBlur}
                onChangeText={onChange}
                value={value}
                placeholderTextColor="#888888"
                style={styles.field}
              />
            )}
            name="title"
          />
          {errors.title && (
            <Text style={styles.errorText}>* Title is required.</Text>
          )}
        </View>

        <Text
          style={[
            styles.label,
            { marginTop: 30, marginBottom: 10, marginLeft: 7 },
          ]}
        >
          Author
        </Text>
        <View style={{ position: "relative" }}>
          <Controller
            control={control}
            rules={{
              required: true,
            }}
            render={({ field: { onChange, onBlur, value } }) => (
              <TextInput
                placeholder="Enter Author"
                onBlur={onBlur}
                onChangeText={onChange}
                value={value}
                style={styles.field}
                placeholderTextColor="#888888"
              />
            )}
            name="author"
          />
        </View>
        <Pressable onPress={handleSubmit(onSubmit)}>
          <LinearGradient
            colors={["#DF00BC", "#9C00E4"]}
            start={[0, 0]}
            end={[1, 0]}
            style={[styles.button, { marginTop: 40 }]}
          >
            {loading ? (
              <ActivityIndicator size="small" color="#fff" />
            ) : (
              <Text style={{ color: "#fff", fontWeight: "600" }}>ADD BOOK</Text>
            )}
          </LinearGradient>
        </Pressable>
        <Link href="/bookList" asChild>
          <Pressable style={{ alignItems: "center", marginTop: 15 }}>
            <Text style={{ color: "#A2A2A2" }}>
              View the list of all available books?{" "}
              <Text style={{ color: "#fff" }}>Book List</Text>
            </Text>
          </Pressable>
        </Link>
        <Toast />
      </ScrollView>
    </>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#000",
    paddingTop: 40,
    paddingHorizontal: 15,
  },
  button: {
    paddingVertical: 22,
    justifyContent: "center",
    alignItems: "center",
    backgroundColor: "#DF00BC",
    borderRadius: 15,
  },
  title: {
    fontSize: 30,
    fontWeight: "500",
    color: "#fff",
    marginTop: 20,
  },
  smallText: {
    color: "#888888",
    fontSize: 13,
    marginTop: 40,
    marginLeft: 7,
  },
  label: {
    color: "#fff",
    fontSize: 17,
  },
  errorText: {
    color: "#9C00E4",
    position: "absolute",
    top: 60,
    left: 7,
  },
  field: {
    backgroundColor: "#171717",
    borderRadius: 15,
    borderColor: "#1F1F1F",
    borderWidth: 1,
    color: "#fff",
    paddingVertical: 18,
    paddingHorizontal: 15,
  },
});
