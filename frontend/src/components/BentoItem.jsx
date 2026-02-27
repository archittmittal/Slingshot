import { motion } from 'framer-motion';

export default function BentoItem({ children, className = '', delay = 0 }) {
    return (
        <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            whileInView={{ opacity: 1, scale: 1 }}
            viewport={{ once: true }}
            transition={{
                duration: 0.5,
                delay,
                ease: [0.23, 1, 0.32, 1]
            }}
            className={`glass kpi-card ${className}`}
        >
            {children}
        </motion.div>
    );
}
