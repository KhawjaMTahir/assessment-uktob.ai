"""
Serializers for Recipe APIS
"""
from decouple import config
import textwrap
from rest_framework import serializers
from .models import Note

from langchain.text_splitter import (
    CharacterTextSplitter,
    RecursiveCharacterTextSplitter,
)
from langchain.llms import OpenAI
from langchain.chains.summarize import load_summarize_chain
from langchain.prompts import PromptTemplate


class NoteSerializer(serializers.ModelSerializer):
    """Serializer for notes."""

    class Meta:
        model = Note
        fields = ["id", "title", "description"]
        read_only_fields = ["id"]

    def create(self, validated_data):
        """Create a note."""
        note = Note.objects.create(**validated_data)

        summary = self.summarize_text(note.description)
        note.summary = summary
        note.save()
        return note

    def update(self, instance, validated_data):
        """Update note."""

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        summary = self.summarize_text(instance.description)
        instance.summary = summary

        instance.save()
        return instance

    def summarize_text(self, text):
        api_key = config("API_KEY")
        llm = OpenAI(api_key=api_key, temperature=0)

        prompt = """Give precise, brief summary of the following: "{text}":"""
        prompt = PromptTemplate(template=prompt, input_variables=["text"])

        chain = load_summarize_chain(llm, chain_type="stuff", prompt=prompt)
        splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        pages = splitter.split_text(text)

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=100
            )
        text = splitter.create_documents(pages)
        summary = chain.run(text)
        summary = textwrap.fill(
            summary, width=100,
            break_long_words=False,
            replace_whitespace=False
        )
        summary = summary.replace("\n", "")

        try:
            return summary
        except Exception:
            return ""


class NoteDetailSerializer(serializers.ModelSerializer):
    """Serializer for notes."""

    class Meta:
        model = Note
        fields = ["id", "title", "description", "summary"]
        read_only_fields = ["id"]
