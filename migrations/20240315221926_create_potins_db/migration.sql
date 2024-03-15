-- CreateEnum
CREATE TYPE "StartUp" AS ENUM ('Theodo', 'TheodoUK', 'TheodoUS', 'BAM', 'Padok', 'Sicara', 'Sipios', 'Hokla', 'Solona');

-- CreateEnum
CREATE TYPE "Permission" AS ENUM ('Admin', 'User');

-- CreateTable
CREATE TABLE "User" (
    "email" TEXT NOT NULL,
    "password" TEXT NOT NULL,
    "firstname" TEXT NOT NULL,
    "lastname" TEXT NOT NULL,
    "startup" "StartUp" NOT NULL,
    "permission" "Permission" NOT NULL,

    CONSTRAINT "User_pkey" PRIMARY KEY ("email")
);

-- CreateTable
CREATE TABLE "Potin" (
    "id" SERIAL NOT NULL,
    "content" TEXT NOT NULL,
    "authorEmail" TEXT NOT NULL,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "concernedUsersGroupEmail" TEXT[],

    CONSTRAINT "Potin_pkey" PRIMARY KEY ("id")
);

-- CreateIndex
CREATE UNIQUE INDEX "User_email_key" ON "User"("email");

-- AddForeignKey
ALTER TABLE "Potin" ADD CONSTRAINT "Potin_authorEmail_fkey" FOREIGN KEY ("authorEmail") REFERENCES "User"("email") ON DELETE RESTRICT ON UPDATE CASCADE;
