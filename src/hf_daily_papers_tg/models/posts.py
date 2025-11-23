from datetime import datetime

from pydantic import BaseModel, Field

from hf_daily_papers_tg.models._escape import escape


class Blog(BaseModel):
    slug: str
    title: str
    upvotes: int
    published_at: datetime = Field(alias="publishedAt")

    @property
    def hf_url(self) -> str:
        return f"https://huggingface.co/blogs/{self.slug}"

    @property
    def hf_hyperlink(self) -> str:
        return f"<a href='{self.hf_url}'>{escape(self.title)}</a>"


class Blogs(BaseModel):
    blogs: list[Blog] = Field(alias="allBlogs")


class ArticleAuthor(BaseModel):
    name: str


class Article(BaseModel):
    published_at: datetime = Field(alias="publishedAt")
    slug: str
    title: str
    upvotes: int
    author: ArticleAuthor = Field(alias="authorData")

    @property
    def hf_url(self) -> str:
        return f"https://huggingface.co/blog/{self.author.name}/{self.slug}"

    @property
    def hf_hyperlink(self) -> str:
        return f"<a href='{self.hf_url}'>{escape(self.title)}</a>"


class CommunityArticlesModel(BaseModel):
    posts: list[Article]
