import { parseStringPromise } from 'xml2js';

const PADDING = '  '; // Define the indentation padding

// Define the type for the XML object
type XmlObject = {
	[key: string]: any;
};

export const tryParseXmlEvent = (input: string): { name: string; content: string } | null => {
	const regex = /<(.+?)>(.*?)<\/\1>/;
	const match = input.match(regex);

	if (!match) {
		return null;
	}

	if (!match[1] || !match[2]) {
		return null; // Return null if the format is not matched
	}

	return {
		name: match[1], // Extracts the agent name
		content: match[2], // Extracts the message content
	};
};

export const tryParseXmlEvents = (input: string): { name: string; content: string }[] | null => {
	const regex = /<(.+?)>(.*?)<\/\1>/g;
	const matches = [...input.matchAll(regex)];

	if (matches.length === 0) {
		return [];
	}

	const result = matches.map((match) => {
		if (match[1] === undefined || match[2] === undefined) {
			return null;
		}
		return {
			name: match[1], // Extracts the agent name
			content: match[2], // Extracts the message content
		};
	});

	if (result.includes(null)) {
		return null;
	}

	return result as { name: string; content: string }[];
};

// Function to format XML
export async function formatXml(xmlString: string): Promise<string> {
	try {
		// Parse the XML string into a JavaScript object using xml2js with explicitArray set to false
		const result: XmlObject = await parseStringPromise(xmlString, {
			trim: true,
			explicitArray: false,
		});
		return buildFormattedXml(result, 0);
	} catch (error) {
		throw new Error(`Error parsing XML: ${error.message}`);
	}
}

// Recursively format the XML object with indentation
function buildFormattedXml(node: XmlObject, level: number = 0): string {
	let formattedXml = '';
	const indent = PADDING.repeat(level);

	for (const key in node) {
		if (Array.isArray(node[key])) {
			// Handle arrays (duplicate elements) by iterating over each element
			node[key].forEach((item: XmlObject) => {
				formattedXml += `${indent}<${key}>\n`;
				formattedXml += buildFormattedXml(item, level + 1);
				formattedXml += `${indent}</${key}>\n`;
			});
		} else if (typeof node[key] === 'object' && node[key] !== null) {
			formattedXml += `${indent}<${key}>\n`;
			formattedXml += buildFormattedXml(node[key], level + 1);
			formattedXml += `${indent}</${key}>\n`;
		} else if (typeof node[key] === 'string' || typeof node[key] === 'number') {
			formattedXml += `${indent}<${key}>${node[key]}</${key}>\n`;
		}
	}

	return formattedXml;
}
