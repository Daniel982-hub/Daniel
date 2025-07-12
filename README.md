import { useState, useContext, createContext } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { motion } from "framer-motion";

const CartContext = createContext();

const productsData = [
  {
    id: 1,
    name: "Creme Facial Natural",
    description: "Hidratação profunda com aloe vera e óleo de jojoba.",
    price: 19.99,
    image: "/images/product1.jpg",
  },
  {
    id: 2,
    name: "Óleo Corporal Orgânico",
    description: "Suaviza e nutre com óleo de coco e lavanda.",
    price: 24.99,
    image: "/images/product2.jpg",
  },
  {
    id: 3,
    name: "Bálsamo Labial Vegano",
    description: "Proteção natural com manteiga de karité.",
    price: 9.99,
    image: "/images/product3.jpg",
  },
];

export default function LojaCuidadosPessoais() {
  const [cart, setCart] = useState([]);

  const addToCart = (product) => {
    setCart((prev) => [...prev, product]);
  };

  const removeFromCart = (index) => {
    setCart((prev) => prev.filter((_, i) => i !== index));
  };

  return (
    <CartContext.Provider value={{ cart, addToCart, removeFromCart }}>
      <div className="min-h-screen bg-rose-50 text-gray-800">
        {/* Header */}
        <header className="bg-white shadow p-4 flex justify-between items-center">
          <h1 className="text-2xl font-bold text-rose-500">BelaNature</h1>
          <nav className="space-x-4">
            <Button variant="ghost">Início</Button>
            <Button variant="ghost">Produtos</Button>
            <Button variant="ghost">Sobre Nós</Button>
            <Button variant="ghost">Contato</Button>
          </nav>
        </header>

        {/* Hero Section */}
        <section className="grid md:grid-cols-2 items-center p-10 gap-6">
          <motion.div
            initial={{ opacity: 0, x: -50 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.8 }}
            className="space-y-4"
          >
            <h2 className="text-4xl font-bold text-rose-600">Cuida de ti naturalmente</h2>
            <p className="text-lg">
              Descobre produtos de cuidados pessoais com ingredientes naturais, sustentáveis e cruelty-free.
            </p>
            <Button className="bg-rose-500 hover:bg-rose-600">Ver Produtos</Button>
          </motion.div>
          <motion.img
            src="/images/skincare-hero.jpg"
            alt="Produtos de cuidados pessoais"
            className="rounded-2xl shadow-xl"
            initial={{ opacity: 0, x: 50 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.8 }}
          />
        </section>

        {/* Produtos em Destaque */}
        <section className="p-10 bg-white">
          <h3 className="text-2xl font-semibold text-center mb-6 text-rose-500">Mais Vendidos</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {productsData.map((product) => (
              <Card key={product.id} className="rounded-2xl shadow">
                <CardContent className="p-4 space-y-2">
                  <img
                    src={product.image}
                    alt={product.name}
                    className="rounded-xl h-48 w-full object-cover"
                  />
                  <h4 className="font-semibold">{product.name}</h4>
                  <p className="text-sm text-gray-600">{product.description}</p>
                  <p className="text-sm font-medium text-rose-500">€{product.price.toFixed(2)}</p>
                  <Button
                    className="w-full bg-rose-500 hover:bg-rose-600"
                    onClick={() => addToCart(product)}
                  >
                    Adicionar ao Carrinho
                  </Button>
                </CardContent>
              </Card>
            ))}
          </div>
        </section>

        {/* Carrinho */}
        <section className="p-6 bg-rose-100">
          <h3 className="text-xl font-semibold mb-4 text-center">Carrinho de Compras</h3>
          {cart.length === 0 ? (
            <p className="text-center text-gray-600">O teu carrinho está vazio.</p>
          ) : (
            <ul className="space-y-4 max-w-xl mx-auto">
              {cart.map((item, index) => (
                <li key={index} className="bg-white p-4 rounded-xl shadow flex justify-between items-center">
                  <div>
                    <p className="font-semibold">{item.name}</p>
                    <p className="text-sm text-gray-600">€{item.price.toFixed(2)}</p>
                  </div>
                  <Button variant="outline" onClick={() => removeFromCart(index)}>
                    Remover
                  </Button>
                </li>
              ))}
            </ul>
          )}
        </section>

        {/* Newsletter */}
        <section className="p-10 bg-rose-100 text-center">
          <h3 className="text-xl font-semibold mb-2">Recebe novidades e promoções</h3>
          <p className="mb-4 text-gray-700">Inscreve-te na nossa newsletter</p>
          <div className="flex justify-center gap-2 max-w-md mx-auto">
            <Input placeholder="Teu email" className="bg-white" />
            <Button className="bg-rose-500 hover:bg-rose-600">Subscrever</Button>
          </div>
        </section>

        {/* Footer */}
        <footer className="p-6 text-center text-sm text-gray-500">
          © 2025 BelaNature. Todos os direitos reservados.
        </footer>
      </div>
    </CartContext.Provider>
  );
}

